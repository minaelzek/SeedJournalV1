# Emotional QA script (TestFlight / pre–App Store)

Run on a **physical device**, staging or production API, **Sign in with Apple**.  
One tester, quiet room, ~25 minutes. Pass/fail gut check: *mature, calm, private — not childish or clinical.*

---

## 1. First open (5 min)

- [ ] Onboarding: three screens feel respectful, not salesy  
- [ ] No tab bar; tree is the home anchor  
- [ ] Copy does not mention streaks, points, or sharing  

## 2. Reflect (5 min)

- [ ] Compose: placeholder “Write freely…”  
- [ ] Save → choice to **Continue reflecting** or **Save & close** (user control)  
- [ ] With AI depth **off** in Settings: no push into reflection thread  

## 3. AI guide (5 min)

- [ ] Assistant tone: curious, not authoritative (“you should”, diagnosis)  
- [ ] Can complete reflection without using all turns  
- [ ] **Save & close** always available  

## 4. Tree & season (3 min)

- [ ] Tree loads without error after save  
- [ ] VoiceOver (optional): stage, season, leaves summarized  
- [ ] If testing winter state: copy is invitational, not “you failed”  

## 5. Memory & patterns (3 min)

- [ ] **Ask** search returns sensible results after pipeline (wait ~10s post-complete)  
- [ ] **Patterns** language is non-diagnostic  

## 6. Trust (4 min)

- [ ] Settings → Privacy policy opens hosted URL  
- [ ] Crisis link opens 988 site  
- [ ] Export produces JSON  
- [ ] Sign out works  

## Fail criteria (block release)

- Mascot / cartoon XP UI appears  
- AI claims medical or therapy role  
- Journal content visible to other users (any social leak)  
- Forced reflection with no dismiss  

Record notes in App Store Connect TestFlight feedback or a private doc.