#!/usr/bin/env python3
"""MARS/100 mission architecture trade study. Python 3 standard library only.
Two-body trajectory, rocket-equation mass sizing, and fleet optimization.
See references.md for physical constants and scenario parameters.
"""
from __future__ import annotations
import csv, json, math, random
from dataclasses import dataclass, asdict
from pathlib import Path

AU_KM = 149597870.7
MU_SUN = 132712440041.27942  # JPL DE440 approx km^3/s^2
MU_EARTH = 398600.435507    # JPL DE440 approx km^3/s^2
EARTH_RADIUS_KM = 6378.137
MARS_ORBIT_AU = 1.523679
G0_KM_S2 = 9.80665 / 1000
DAY_SEC = 86400

@dataclass
class Assumptions:
    target_t: float = 100
    module_t: float = 25
    leo_alt_km: float = 300
    leo_delivery_cap_t: float = 150
    tanker_net_prop_t: float = 80
    small_dry_fixed_t: float = 16
    large_dry_fixed_t: float = 30
    dry_per_payload: float = 0.12
    isp_tmi_s: float = 380
    isp_edl_s: float = 330
    edl_terminal_dv_kms: float = 0.60
    cargo_launch_musd: float = 90
    tanker_launch_musd: float = 75
    small_lander_musd: float = 80
    large_lander_musd: float = 160
    p_launch: float = 0.98
    p_transfer: float = 0.96
    p_edl_small: float = 0.92
    p_edl_large: float = 0.85
    min_reliability: float = 0.95
    campaign_windows: int = 2
    # Surrogate tech demonstration reliability: independent events, optimistic


def trajectory(leo_alt_km: float=300) -> dict:
    re = AU_KM
    rm = MARS_ORBIT_AU * AU_KM
    at = (re+rm)/2
    ve = math.sqrt(MU_SUN/re)
    vm = math.sqrt(MU_SUN/rm)
    vh1 = math.sqrt(MU_SUN*(2/re-1/at))
    vh2 = math.sqrt(MU_SUN*(2/rm-1/at))
    vinf_e = abs(vh1-ve)
    vinf_m = abs(vm-vh2)
    leo = EARTH_RADIUS_KM+leo_alt_km
    dv = math.sqrt(vinf_e**2+2*MU_EARTH/leo)-math.sqrt(MU_EARTH/leo)
    transfer_days = math.pi*math.sqrt(at**3/MU_SUN)/DAY_SEC
    earth_period_days = 2*math.pi*math.sqrt(re**3/MU_SUN)/DAY_SEC
    mars_period_days = 2*math.pi*math.sqrt(rm**3/MU_SUN)/DAY_SEC
    synodic_days= 1/(1/earth_period_days-1/mars_period_days)
    angle = 180 - 360*(transfer_days/mars_period_days)
    return dict(transfer_days=transfer_days, tmi_dv_kms=dv,
                earth_vinf_kms=vinf_e, mars_vinf_kms=vinf_m,
                heliocentric_burn_sum_kms=vinf_e+vinf_m,
                phase_angle_deg=angle, synodic_days=synodic_days,
                earth_period_days=earth_period_days,
                mars_period_days=mars_period_days)


def vehicle(payload_t:float, a:Assumptions) -> dict:
    tr=trajectory(a.leo_alt_km)
    fixed = a.small_dry_fixed_t if payload_t <= a.module_t + 1e-9 else a.large_dry_fixed_t
    dry = fixed + a.dry_per_payload*payload_t
    final_mass = dry+payload_t
    edl_mass = final_mass*math.exp(a.edl_terminal_dv_kms/(G0_KM_S2*a.isp_edl_s))
    tmi_mass = edl_mass*math.exp(tr['tmi_dv_kms']/(G0_KM_S2*a.isp_tmi_s))
    edl_prop = edl_mass - final_mass
    tmi_prop = tmi_mass - edl_mass
    total_prop = edl_prop+tmi_prop
    tankers = max(0, math.ceil((tmi_mass-a.leo_delivery_cap_t-1e-9)/a.tanker_net_prop_t))
    direct_feasible = tmi_mass <= a.leo_delivery_cap_t+1e-9
    refuel_feasible = final_mass <= a.leo_delivery_cap_t+1e-9
    return dict(payload_t=payload_t,dry_t=dry, landed_mass_t=final_mass,
                edl_prop_t=edl_prop,tmi_prop_t=tmi_prop,total_prop_t=total_prop,
                required_leo_mass_t=tmi_mass, direct_feasible=direct_feasible,
                refuel_feasible=refuel_feasible, tanker_launches=tankers,
                required_refuel_t=max(0,tmi_mass-a.leo_delivery_cap_t),
                available_tanker_prop_t=tankers*a.tanker_net_prop_t,
                tmi_dv_kms=tr['tmi_dv_kms'])


def binomial_tail(n:int, p:float, k:int)->float:
    return sum(math.comb(n,j)*p**j*(1-p)**(n-j) for j in range(k,n+1))


def expected_capped_t(n:int, p:float, module_t:float, target_t:float)->float:
    return sum(math.comb(n,j)*p**j*(1-p)**(n-j)*min(target_t,j*module_t) for j in range(n+1))


def architectures(a:Assumptions)->list[dict]:
    tr=trajectory(a.leo_alt_km)
    small=vehicle(a.module_t,a)
    large=vehicle(a.target_t,a)
    needed_modules=math.ceil(a.target_t/a.module_t)
    p_small=a.p_launch*a.p_edl_small
    p_large=(a.p_launch**(1+large['tanker_launches']))*a.p_transfer*a.p_edl_large
    small_cost=a.cargo_launch_musd+a.small_lander_musd
    large_cost=a.cargo_launch_musd+large['tanker_launches']*a.tanker_launch_musd+a.large_lander_musd
    candidates=[]
    for n in range(needed_modules,10):
        candidates.append(dict(id=f'small_{n}',label=f'{n} × {a.module_t:g}t landers',family='small',
            units=n, module_t=a.module_t, nominal_t=n*a.module_t,
            launches=n, tankers=0, 
            cost_musd=n*small_cost, 
            success_probability=binomial_tail(n,p_small,needed_modules),
            expected_useful_t=expected_capped_t(n,p_small,a.module_t,a.target_t),
            feasible=small['direct_feasible'],
            windows=1 if n==needed_modules else a.campaign_windows,
            per_vehicle_leo_t=small['required_leo_mass_t']))
    for n in range(1,5):
        candidates.append(dict(id=f'large_{n}',label=f'{n} × {a.target_t:g}t refueled landers',family='large',
            units=n,module_t=a.target_t,nominal_t=n*a.target_t,
            launches=n*(1+large['tanker_launches']), tankers=n*large['tanker_launches'],
            cost_musd=n*large_cost,
            success_probability=1-(1-p_large)**n,
            expected_useful_t=a.target_t*(1-(1-p_large)**n),
            feasible=large['refuel_feasible'],
            windows=1 if n==1 else a.campaign_windows,
            per_vehicle_leo_t=large['required_leo_mass_t']))
    feasible=[x for x in candidates if x['feasible'] and x['success_probability'] >= a.min_reliability]
    optimal=min(feasible,key=lambda x:x['cost_musd']) if feasible else None
    base=[next(c for c in candidates if c['id']==id) for id in ('small_4','large_1','small_6')]
    for x in base:
        x['cost_per_expected_useful_t_musd'] = x['cost_musd']/x['expected_useful_t']
        x['cost_per_target_t_musd'] = x['cost_musd']/a.target_t
        x['target_achieved'] = x['feasible'] and x['success_probability']>=a.min_reliability
        x['arrival_days'] = tr['transfer_days'] + (x['windows']-1)*tr['synodic_days']
    return [base,candidates,optimal,dict(p_small=p_small,p_large=p_large,small=small,large=large,trajectory=tr)]


def sensitivity(a:Assumptions)->list[dict]:
    records=[]
    for edl in [0.75,0.80,0.85,0.90,0.92,0.94,0.96,0.98]:
        for tanker_cost in [40,60,75,90,110,130,150]:
            b=Assumptions(**{**asdict(a),'p_edl_small':edl,'tanker_launch_musd':tanker_cost})
            _,_,best,_=architectures(b)
            records.append(dict(p_edl_small=edl,tanker_launch_musd=tanker_cost,
                                optimal=best['id'] if best else 'none',
                                optimal_musd=best['cost_musd'] if best else None))
    return records


def validate():
    a=Assumptions()
    tr=trajectory()
    assert abs(tr['transfer_days']-259)<3, tr
    assert 3.4<tr['tmi_dv_kms']<3.9, tr
    assert 740<tr['synodic_days']<820
    x=vehicle(25,a)
    assert x['direct_feasible'], x
    assert not vehicle(100,a)['direct_feasible']
    assert vehicle(100,a)['tanker_launches']==4
    assert abs(binomial_tail(4,1,4)-1)<1e-12
    assert abs(binomial_tail(4,0.9,4)-0.9**4)<1e-12
    assert abs(binomial_tail(6,0.9,4)-0.98415)<1e-6
    base,candidates,optimal,aux=architectures(a)
    assert optimal is not None
    assert optimal['id']=='small_6', optimal
    assert abs(sum(math.comb(6,j)*0.9**j*.1**(6-j) for j in range(7))-1)<1e-12
    return True


def main():
    validate()
    a=Assumptions()
    base,candidates,optimal,aux=architectures(a)
    root=Path(__file__).resolve().parent
    result=dict(metadata=dict(name='MARS/100',date='2026-11-20',scope='Conceptual mass and risk trade study',
        warning='No validated Mars landing model, spacecraft design, launch price, or mission success rate'),
        assumptions=asdict(a),trajectory=aux['trajectory'],vehicles=dict(small=aux['small'],large=aux['large']),
        unit_success=dict(small=aux['p_small'],large=aux['p_large']),
        comparison=base,design_space=candidates,selected_optimum=optimal,sensitivity=sensitivity(a))
    (root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    with open(root/'comparison.csv','w',newline='') as f:
        fields=['id','label','units','nominal_t','launches','tankers','cost_musd','success_probability','expected_useful_t','cost_per_expected_useful_t_musd','target_achieved','windows','arrival_days']
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(base)
    with open(root/'design_space.csv','w',newline='') as f:
        fields=['id','label','family','units','nominal_t','launches','tankers','cost_musd','success_probability','expected_useful_t','feasible','windows']
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(candidates)
    with open(root/'sensitivity.csv','w',newline='') as f:
        fields=['p_edl_small','tanker_launch_musd','optimal','optimal_musd']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(result['sensitivity'])
    print('MARS/100 BASELINE', 'transfer days',round(aux['trajectory']['transfer_days'],2),
          'TMI delta-v',round(aux['trajectory']['tmi_dv_kms'],3))
    for x in base:
        print(f"{x['label']:32}  cost ${x['cost_musd']:.0f}M; P(>=100t)={x['success_probability']:.4%}; {x['launches']} launches")
    print('OPTIMUM (under toy assumptions):', optimal['label'], f"${optimal['cost_musd']:.0f}M")

if __name__=='__main__': main()
