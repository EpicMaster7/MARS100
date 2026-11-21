# MARS/100: 3–5 minute recorded walkthrough

**Practical setup:** Open `walkthrough.pptx` or screen-share `dashboard.html` and follow these sections. Approx. 4 minutes at a comfortable speaking pace. Run `python3 model.py` once beforehand if you'd like to show reproducibility. **Review the model first and adapt this to describe only steps you personally understand or performed.**

## 0:00–0:35 | Slides 1–2: The question

"For this exploration, I chose aerospace mission architecture. I wanted to know how a mission planner would decide between sending cargo to Mars in one massive spacecraft or in a fleet of smaller ones. My goal was to identify the least expensive conceptual architecture for landing at least one hundred metric tons of useful cargo, while meeting a ninety-five percent modeled probability of fully delivering that target. I compared three approaches: direct small-lander launches, one large lander refueled in Earth orbit, and a redundant pre-deployed fleet."

## 0:35–1:15 | Slide 3: Orbital mechanics

"I started with orbital mechanics. A spacecraft can't fly directly to where Mars is today. Earth and Mars orbit the Sun, and the spacecraft follows a transfer orbit. Using a simplified Hohmann transfer, I calculated about two hundred fifty-nine days of flight, around forty-four degrees of Mars lead angle at departure, and a roughly three-point-five-nine kilometer-per-second burn to leave a three-hundred-kilometer Earth parking orbit. That last number comes from the parking-orbit injection calculation, and is different from the heliocentric velocity changes. NASA JPL's published teaching example gives almost the same transfer duration."

## 1:15–1:55 | Slide 4: Mass sizing and three designs

"I then worked backwards with the rocket equation. It relates delta-v and engine efficiency to how much propellant the spacecraft needs. In my assumed mass model, a twenty-five-ton cargo lander needs about one hundred thirty-nine tons in Earth orbit before the departure burn. That fits inside the assumed one-hundred-fifty-ton launch limit. A single one-hundred-ton lander needs about four hundred forty-eight tons before departure, which requires four additional tanker flights in the model. These masses are a simplified scenario, not validated spacecraft designs."

## 1:55–2:35 | Slide 5: The result

"Here is the actual comparison. Four direct twenty-five-ton landers cost an assumed six hundred eighty million dollars and have about a sixty-six percent chance of landing the full target. The large refueled option is cheapest at five hundred fifty million, but its modeled success probability is about seventy-four percent. Six small landers cost just over one billion, and have roughly ninety-eight and a half percent modeled probability of landing at least four of the six modules, which adds up to one hundred tons. So with a ninety-five percent reliability requirement, six small landers are the cheapest qualifying design in this model. Without that requirement, the big refueled vehicle wins on cost."

## 2:35–3:20 | Slides 6–7: A problem and sensitivity

"The biggest difficulty was that real Mars landing capability and future launch pricing aren't known well enough to justify definitive costs and probabilities. In fact, NASA's recent technical publication says successful missions have historically landed payloads of about one ton or less. I handled that by labeling dry masses, failure probabilities, prices and terminal landing requirements as hypothetical inputs, then making them adjustable. The dashboard shows how changing the probability of a successful small-lander descent, tanker pricing or descent delta-v can change the recommended architecture. For example, six small landers stop reaching ninety-five percent modeled reliability if the terminal landing success assumption drops below about eighty-six percent."

## 3:20–4:00 | Slide 8: What I learned

"The most interesting insight was how the objective changes the answer. Optimizing total cost favors consolidation into one large spacecraft in my baseline assumptions. Optimizing cost under a stringent reliability threshold favors redundancy. The real challenge is that redundancy only works as the model predicts if failures are sufficiently independent. A common design flaw could affect all six vehicles. I'd next research Mars entry and descent technology, add correlated failure scenarios, improve the actual spacecraft mass budget, and use date-specific trajectory software such as NASA GMAT. The result is an early architecture trade study, not a flight-qualified mission."

## 4:00–4:15 | Optional demonstration

"If you look at the live model, I can adjust the small lander's landing-success assumption. At ninety-two percent, the six-lander architecture clears the confidence requirement, but lower values require another lander. That was my biggest takeaway: the best architecture is inseparable from the assumptions and constraints."

---

**Recording checklist:** Show slide deck or browser; clearly display architecture comparison and at least one changed slider; briefly say what the formulas represent; explicitly describe a limitation and one thing learned; record yourself with QuickTime, Loom or Zoom, then submit the recording with `dashboard.html` and screenshots.

**Integrity note:** This script describes the prepared model. The project includes significant AI-assisted implementation. Do not assert you manually spent four hours coding it if that did not happen. You can accurately say you explored, reviewed and presented an AI-assisted model after doing the corresponding work.
