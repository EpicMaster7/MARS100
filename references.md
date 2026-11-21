# Sources and model parameters

Accessed 2026-11-20. Sources support underlying science and research context. Vehicle economics and mission probabilities are adjustable scenario inputs.

1. **NASA JPL Education, "Let's Go to Mars! Calculating Launch Windows"**  
   https://www.jpl.nasa.gov/edu/resources/lesson-plan/lets-go-to-mars-calculating-launch-windows/  
   NASA JPL describes a Hohmann transfer taking approximately 259 days and a 44° Mars lead angle under circular-orbit assumptions. Corroborates our independently computed 258.87 days and 44.34°.

2. **NASA Glenn Research Center, "Ideal Rocket Equation"**  
   https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/  
   Basis for the mass ratio `m_initial/m_final = exp(Δv/(g0 Isp))`. The assumed 380s and 330s engine Isp values are scenario inputs, not drawn from this source.

3. **JPL Solar System Dynamics, "Astrodynamic Parameters"**  
   https://ssd.jpl.nasa.gov/astro_par.html  
   Source of approximate Sun and Earth gravitational parameters used in orbital transfer and injection calculations.

4. **NASA NSSDC, "Mars Fact Sheet"**  
   https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html  
   Source for Mars's ~1.524 AU average orbital distance.

5. **NASA Technical Reports Server (NTRS), "NASA's Strategic Analysis Cycle 2021 (SAC21) Human Mars Architecture," 2022**  
   https://ntrs.nasa.gov/citations/20220002632  
   A NASA study considered three approximately 25t Mars Descent Systems pre-deployed as cargo infrastructure. These were conceptual systems within an architecture study, and NASA explicitly described the proposal as an option rather than an adopted program.

6. **NASA Technical Reports Server (NTRS), Bryan Palaszewski, "Mars Landing Vehicles: Descent and Ascent Propulsion Design Issues," September 30, 2026**  
   https://ntrs.nasa.gov/citations/20260006975  
   Notes actual successful Mars landing payloads to date of approximately 1t, compared with conceptual 5–25t future human mission payloads. This is a key caveat to any claim of feasible high-mass landing.

7. **NASA Science, "Chapter 4: Trajectories"**  
   https://science.nasa.gov/learn/basics-of-space-flight/chapter4-1/  
   Explains approximate 25-month Earth–Mars minimum-energy launch opportunities.

8. **SpaceX, "Starship" (vehicle overview)**  
   https://new.spacex.com/vehicles/starship  
   Provides contemporary design context for larger-than-100t orbital transport ambitions. **Our 150t LEO cap is an abstract launcher scenario, not a certified Starship capacity or a promise that its tankers could net 80t of orbital propellant.**

## Scenario inputs

- 150t cargo-vehicle-to-LEO delivery cap and 80t net refueling capacity.
- 16t/30t fixed dry masses plus 12% of payload.
- 0.60 km/s terminal descent delta-v and 330s landing-engine Isp.
- 380s TMI propulsion Isp.
- Four illustrative cost terms in the README.
- Cargo launch, refueling and small/large EDL success probabilities.
- Independence of failures; physical ability to deploy 6 large landers over two launch windows.

These inputs drive the optimization and can be changed in the interactive dashboard.
