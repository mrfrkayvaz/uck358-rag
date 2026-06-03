# *Tactical Airplane Maneuverability*

Tactical airplaneshave alwayshad special stability and control problemsbecause of the extreme maneuversrequired of them. The rapid aileron roll, the sharp pullup, and the rapid turn entry all present special problems. Some examples are the level of rolling velocity actually required, overcontrol in pullups, and badly coordinated turn entries. Finally, controlled flight at anglesof attack beyond the stall isa new field of required maneuvers for tactical airplanes.

#### **10.1 How Fast Should Fighter Airplanes Roll?**

Fighter roll capability became a crucial question during the early days of World War II. Many allied fighter airplanescarried gun camerasinto combat. Gun camerasare movie cameraspointed in the direction of the ship'sfixed-wing guns. Moviesare taken as long as the firing trigger was pressed, witnessing hits (or misses) on enemy airplanes or missiles. Gun cameras carried on Curtiss P-40s and North American P-51 s witnessed interesting momentsin dogfightsand bore out pilots' accountsof lossin combat advantages due to relatively low ratesof roll on the U.S. aircraft.

Some Axis aircraft, particularly the Mitsubishi Zero at low airspeeds, would feint a roll in one direction and then roll rapidly in the other direction. The horizon or cloud background in the gun camera pictures would show the Allied airplane following the feint, a bit slower perhaps, then be left behind as the Zero did a rapid roll in the opposite direction and disappeared from the gun camera's view.

Clearly, high-rolling velocity performance wasneeded at dogfight airspeedsin order not to lose firing opportunities when in the favorable trailing position. At the low end of the fighter airspeed range the Gilruth/NACA criterion pb/2V = 0.07 wasa reasonable guide, although higher levels, up to 0.10, were considered. Higher pb/2V levelscould be attained with extra-large ailerons. But in early World War II days, before hydraulically powered controls, the wide-chord, long-span ailerons that provided high pb/2V valuesmeant high stick forces, restricting rolling velocities at high airspeeds.

In other words, an airplane could be designed for fast rolling performance at either low airspeeds, say below 200 knots, or high airspeeds, but not both. The Curtiss P-40 was typical in that itsmaximum rolling velocity of 95 degreesper second occurred at an airspeed of 270 milesper hour. At 400 milesper hour (not shown in Fig. 10.1) maximum available rolling velocity dropped to 65 degrees per second, limited by a nominal 30-pound stick force.

Restricted maneuverability due to high stick forces started an intense research program on both sides of the Atlantic. The British seemed to have had the innovative edge, coming up with two significant stick force reduction schemes: the spring tab, ultimately used on the Hawker Tempest, and the beveled-edge control surface. The history of these devices is given in Chapter 5, "Managing Control Forces." Beveled-edge ailerons worked quite well for the P-51 Mustang, almost doubling the available rate of roll.

![Chapter 10 - Figure 1](../assets/chapter10/_page_1_Figure_1.jpeg)

**Figure 10.1** Rolling velocitiesobtainable with 50 poundsof stick force for a number of World War II fighter airplanes, all at an altitude of 10,000 feet. These data were heavily classified during the war. (From Toll, NACA Rept. 868, 1947)

Hydraulic power assistance came into the picture for fighter-type airplanes only at the very end of World War II, on the aileronsof the late version Lockheed P-38J Lightning. However, once power controlsbecame common, in about 1950, stick force limitationsto rate of roll were overcome. Now the only limits were hydraulic system capacity, control system and wing strength, wing torsional stiffness, and the inertial coupling phenomenon discussed in Chapter 8. The military specification version of that period reflected these new capabilities. Fighter roll rates up to 360 degrees per second were required. A limiting factor in fighter roll maneuverability at high airspeedsand low altitudesiswing twist, treated in Chapter 19, "The Elastic Airplane."

#### **10.2 Air-to-Air Missile-Armed Fighters**

A price hasto be paid for extreme rolling performance in termsof demandson hydraulic system size and flow rate and on structural weight required for strength and stiffness. This led to a new controversy. As in the days of P-40s versus Zeros, high roll rates were important in dogfight gun-versus-gun battles.

But what about fighters that merely fired air-to-air missiles? Sparrow I and Sidewinder air-to-air missiles both went into service in 1956. Clearly, the missiles themselves can do the end-game maneuvering, to veer left and right, climb and dive, following any feintsby the airplane being attacked. Penalizing missile-armed fighters so that they could carry out dogfight tacticsmight be asfoolish asit would have been to require Army tank crewsto wear cavalry spurs.

The drive to reduce fighter airplane rolling requirements because of the advent of missilearmed fighters was led on the technical side by a former NACA stability and control engineer who had risen to a high administrative level. The then USAF Director of Requirements weighed in with a letter stating flatly that the F-103 would be the last USAF manned fighter airplane.

The need for high levelsof fighter airplane rolling performance wasargued back and forth at Wright Field and the Naval Air Systems Command until the issue was settled by the Vietnam War of 1964 –1973. U.S. fighterswent into that conflict armed with both Sparrow and Sidewinder air-to-air missiles. Nevertheless, they found themselves dogfighting with Russian-built fighters. The reason that aerial combat was carried out at dogfighting ranges was that visual target identification and missile lock-before-launch doctrines were found to be needed, to avoid missile firings at friendly targets. Ranges for positive visual identification were so small that engagements quickly became dogfights. High roll rates were once more in favor. Of course, dogfighting capability meant that guns could still be used effectively on missile-carrying fighters.

# **10.3 Control Sensitivity and Overshoots in Rapid Pullups**

When powerful, light longitudinal controlsbecame available for tactical airplanes, the problems of oversensitivity, sluggishness, normal acceleration overshoots, and pilotinduced oscillations appeared. Airplane-pilot coupling, also called pilot-induced oscillations, isproperly dealt with asthe combination of the dynamicsof human pilotswith that of their airplanes (see Chapter 21). However, oversensitivity, sluggishness, and overshoots may be understood in simpler terms, that of the airplane alone, without specifically involving pilot dynamics. A fundamental indicator of airplane-alone pitch response is the pitch rate transfer function for elevator or stabilizer control inputs (Figure 10.2). Under the usual constant-airspeed assumption, this function has a second-order denominator and a first-order numerator. Although a pure delay may be added, only three parameters are involved: the frequency and damping ratio of the second-order term and the time constant of the first-order term. A number of criteria on oversensitivity, sluggishness, and overshoots deal with thisairplane-alone transfer function.

# **10.3.1** *Equivalent Systems Methods*

Equivalent systems or low-order approaches refer to fitting an airplane-alone transfer function to the complex dynamics of actual airplane and flight control systems. Hodgkinson, La Manna, and Hyde (1976) are generally referenced as the origin of the

| input   | mechanism | output   |
|---------|-----------|----------|
| x       | or        | y        |
| (cause) | system    | (effect) |

A mechanism or complete system with input x and output y defined by the differential equation

$$\begin{aligned} \left[ \frac{\mathbf{d}^{\mathrm{m}+n}}{\mathbf{d}t^{\mathrm{m}+n}} + \mathbf{b}\_{1} \frac{\mathbf{d}^{\mathrm{m}+n-1}}{\mathbf{d}t^{\mathrm{m}+n-1}} + \dots + \mathbf{b}\_{\mathrm{m}+\mathrm{n}-1} \frac{\mathbf{d}}{\mathbf{d}t} + \mathbf{b}\_{\mathrm{m}+\mathrm{n}} \right] \mathbf{y}(\mathbf{t}) \\ = \mathbf{K} \left[ \frac{\mathbf{d}^{\mathrm{n}}}{\mathbf{d}t^{\mathrm{n}}} + \mathbf{a}\_{1} \frac{\mathbf{d}^{\mathrm{n}-1}}{\mathbf{d}t^{\mathrm{n}-1}} + \dots + \mathbf{a}\_{\mathrm{n}-1} \frac{\mathbf{d}}{\mathbf{d}t} + \mathbf{a}\_{\mathrm{n}} \right] \mathbf{x}(\mathbf{t}) \end{aligned}$$

can be represented by the transfer function in the Laplace variable s:

$$\frac{\mathbf{Y}(\mathbf{s})}{\mathbf{X}(\mathbf{s})} = \frac{\mathbf{K}(\mathbf{s}^{\mathbf{n}} + \mathbf{a}\_1 \mathbf{s}^{\mathbf{n}-1} + \dots + \mathbf{a}\_{\mathbf{n}-1} \mathbf{s} + \mathbf{a}\_\mathbf{n})}{\mathbf{s}^{\mathbf{m}+\mathbf{n}} + \mathbf{b}\_1 \mathbf{s}^{\mathbf{m}+\mathbf{n}-1} + \dots + \mathbf{b}\_{\mathbf{m}+\mathbf{n}-1} \mathbf{s} + \mathbf{b}\_{\mathbf{m}+\mathbf{n}}}.$$

An example is the pitch rate transfer function for elevator or stabilizer inputs, with the airspeed degree of freedom suppressed:

$$\frac{\mathbf{q}(\mathbf{s})}{\delta(\mathbf{s})} = \frac{(\mathbf{M}\_{\delta} + \mathbf{Z}\_{\delta}\mathbf{M}\_{\Psi})\mathbf{s} + \mathbf{Z}\_{\delta}\mathbf{M}\_{\mathbf{w}} - \mathbf{M}\_{\delta}\mathbf{Z}\_{\mathbf{w}}}{\mathbf{s}^{2} - (\mathbf{U}\_{\mathbf{o}}\mathbf{M}\_{\Psi} + \mathbf{Z}\_{\mathbf{w}} + \mathbf{M}\_{\mathbf{q}})\mathbf{s} + \mathbf{M}\_{\mathbf{q}}\mathbf{Z}\_{\mathbf{w}} - \mathbf{U}\_{\mathbf{o}}\mathbf{M}\_{\mathbf{w}}}.$$

In these equations,

a,b = constants K = gain M<sup>δ</sup> , Zw, etc. = control and stability derivatives q = pitching velocity s = Laplace variable Uo = forward speed δ = elevator or stabilizer deflection.

**Figure 10.2** The transfer function concept. (Adapted from *Aircraft Dynamics and Automatic Control*, by McRuer, Ashkenas, and Graham, Princeton U. Press, 1973)

equivalent systems method. The McRuer, Ashkenas, and Graham approximate factors, with time delay added from variable stability NT-33 tests carried out by Dante DiFranco, were used to match frequency responses of the Neal-Smith data set.

Transfer function criteria, for the airplane alone or the equivalent system, have the authority of a great deal of analysis, simulator, and flight research. Excellent reviews of this field are given by Gibson (1995) and by Hoh and Mitchell (1996). While the original work on transfer-function–based criteria was concerned with tactical airplanes, these criteria were used as well in the flight control designs of modern transport airplanes such as the Boeing 777 (Ward, 1996) and the Airbus series, starting with the A320.

### **10.3.2** *Criteria Based on Equivalent Systems*

A brief summary of the criteria based on airplane-alone or equivalent system transfer functionsisasfollows:

![Chapter 10 - Figure 1](../assets/chapter10/_page_4_Figure_1.jpeg)

**Figure 10.3** Example of an early iso-opinion chart for the longitudinal short-period mode. This one wasderived from flight testsof the variable-stability F-94F airplane. (Mazza, Becker, Cohen, and Spector, NADC Report ED-6282, 1963)

- **Frequency-Damping Boundaries** Historically, the earliest findings on pitch sensitivity and sluggishness from variable-stability airplane research was bullseye–type pilot opinion contoursof the two denominator parametersof the pitch transfer function: natural frequency and damping ratio (Figure 10.3). This work was done by Robert P. Harper and his associates at the Cornell Aeronautical Laboratory in the early 1950s. Gibson (1995) comments that these boundaries ignore the attitude response. He suggests adding quantitative information on attitude response, such as delay, dropback (see subsequent definition), and overshoot.
- **Numerator Time Constant Requirements** The numerator time constant, *T*θ2, controls the rapidity with which attitude changes result in flight path changes. Shorter values, corresponding to high lift curve slope and light wing loadings, give faster path responses and lower, or better, Cooper-Harper ratings. However, the benefitsof low numerator time constantsare mainly confined to landing approach control and have little to do with tactical airplane maneuverability.
- **Bihrle's Control Anticipation Parameter** By far the most successful of the criteria based on pitch transfer function parameters is the control anticipation

![Chapter 10 - Figure 1](../assets/chapter10/_page_5_Figure_1.jpeg)

**Figure 10.4** MIL-F-8757C short-period mode equivalent natural frequency and CAP (Control Anticipation Parameter) requirements(1980).

- parameter, or CAP (Bihrle, 1966). CAP isthe ratio of the airplane'sinitial pitch acceleration in an abrupt pullup to the steady-state normal acceleration produced. The initial pitch acceleration letsthe pilot anticipate the final acceleration response. It turned out that CAP also could be expressed as the ratio of the pitch natural frequency to a function of the numerator time constant. In that form CAP appearsin MIL-F-8785C (Figure 10.4) and isalso referenced in the newer MIL-STD-1797. CAP isaugmented by requirementson damping ratio and time delay (Figure 10.5).
- **Gautrey and Cook's Generic CAP, or GCAP** The CAP criterion can be extended to augmented aircraft without recourse to equivalent systems. The generic CAP criterion, or GCAP, usesdifferent parametersthan CAP but hasthe same interpretation. GCAP is neither based on short-period transfer function parameters nor does it require a steady-state normal acceleration, as does CAP. GCAP parametersare well defined even for fully augmented pitch control systems such as are found on the Boeing 777 and Airbus A320 –A340 series.

![Chapter 10 - Figure 1](../assets/chapter10/_page_6_Figure_1.jpeg)

**Figure 10.5** Equivalent systems requirements for longitudinal short-period damping and time delay. (From MIL-F-8785C, Nov. 1980)

- **Bandwidth Criterion** Thisisa criterion based on the transfer function for pitch attitude asan output for control force asan input. The pitch attitude bandwidth isdefined arbitrarily asthe lower of two frequencies: the gain bandwidth frequency, at which there isa 6-db gain margin, and the phase bandwidth frequency, at which there isa 45-degree phase margin. An additional factor is the phase delay, which accounts for phase lags introduced by higher frequency components, such as control actuators. A typical bandwidth criterion chart is reproduced in Figure 10.6. The bandwidth criterion is considered significant, although the exact shape of suitable boundaries is still a research matter.
- **Gibson Nichols Chart Criterion** This criterion defines satisfactory and unsatisfactory flying qualitiesregionsin the Nicholsplane of open-loop transfer function gain and phase. An early version of this criterion is shown in Figure 10.7. The concept of attitude dropback appearson the chart, a term defined subsequently.

# **10.3.3** *Time Domain–Based Criteria*

Time domain response specifications get around the need for equivalent systems. A standard time domain response form was used in the 1987 version of the U.S. flying

![Chapter 10 - Figure 1](../assets/chapter10/_page_7_Figure_1.jpeg)

**Figure 10.6** Example pitch attitude bandwidth/phase delay criterion, with test results. (From Field and Rossitto, 1999).

![6** Example pitch attitude bandwidth/phase delay criterion, with test results. (](../assets/chapter10/_page_7_Figure_3.jpeg)

**Figure 10.7** Pilot evaluation of pitch response using Gibson Nichols chart template. (From Blight 1996)

| Level | Nonterminal Flight Phases  Terminal Flight Phases |         |        |        |
|-------|---------------------------------------------------|---------|--------|--------|
|       | Min △t                                            | Max △t  | Min △t | Max At |
|       | 9/V+                                              | 500/V7  | 9/V+   | 200/V+ |
| 2     | 3.2/VT 1                                          | 1600/V+ | 3.2/VT | 645/V+ |

| RISE | TIME | LIMITS |
|------|------|--------|
|------|------|--------|

![Chapter 10 - Figure 1](../assets/chapter10/_page_8_Figure_4.jpeg)

**Figure 10.8** Generic pitch rate response to abrupt control input. This type of transient response description hasthe advantage of applying to high-order stability-augmented aswell asunaugmented airplanes. (From Mil Standard MIL-STD-1797, 1987)

qualities standard, MIL-STD-1797 (Figure 10.8). Other time domain response criteria have been proposed, as follows:

- **The C\* Parameter** L. G. Malcolm and H. N. Tobie originated the C\* parameter, to blend normal acceleration and pitch rate responses to pitch control input. C\* is actually a weighted, linear combination of the two responses, akin to the weighted performance indices used in optimization calculations.
- **The Time Response Parameter** Some yearslater, C. R. Abramsenlarged on the C\* parameter approach with a time response parameter that includes time delay in addition to the earlier normal acceleration and pitch rate terms.
- **Gibson Dropback Criterion** Thisrefersto the pitch attitude change following a commanded positive pulse in airplane angle of attack. Pitch attitude increases during the pulse. A pitch attitude decrease after the pulse ends is called a dropback. A slight dropback is associated with fine tracking. A large or negative dropback (pitch overshoot) creates unsatisfactory pitch short-period behavior.
- **Special Time Response Boundaries** Upper and lower boundariesfor longitudinal response was a still later specification form, used widely for landing approach responses in addition to up-and-away flying. The space shuttle Orbiter's longitudinal control response is governed by such boundaries (Figure 10.9), apparently established in simulation.

Gibson (2000) comments that the upper boundary in particular severely limits rapid acquisition of angle of attack change in response to pitch demand and was responsible for space shuttle touchdown problems. He says further:

![Chapter 10 - Figure 1](../assets/chapter10/_page_9_Figure_1.jpeg)

**Figure 10.9** An example of a time response boundary. The pitch rate response to a step-type manipulator input must lie between the boundaries. Pitch rate response *q* is normalized by the steady-state value *qss*. This particular time response boundary applies to the space shuttle Orbiter. (From Mooij, AGARD LS 157, 1988)

The UK HOTOL project (a horizontal take off Shuttle equivalent) wasstudied at Warton . . . By designing to optimum piloted pitch response dynamics, i.e., with a rapid flight path response and hence considerable pitch rate overshoot, accurate automatic touchdown was easily achieved in simulation.

Further progress in understanding and improving longitudinal maneuverability has made use of closed-loop studies using the human pilot model (see Chapter 21).

# **10.4 Rapid Rolls to Steep Turns**

Effective use of aileronsfor rapid rollsto steep turnsrequiresnot only good roll response but also coordination, or the suppression of adverse yaw. The airplane's lift vector should remain close to the airplane's plane of symmetry during the roll and turn entry. The ball of the turn and slip indicator (see Chapter 15, Sec. 10.1) will then remain close to center, and the maneuver will be called coordinated. An alternate coordination condition is suppression of sideslip, which puts the velocity vector in the airplane's plane of symmetry.

Starting with the 1943 Gilruth requirements for satisfactory flying qualities, coordination requirementswere examined in rapid aileron rollswith the rudder held fixed at the initial trim position. The peak sideslip excursion and the phase angle of the Dutch roll component of the excursion were correlated with pilots' ratings and used as the basis of U.S. Air Force coordination requirements.

More recent studies of tactical airplane roll response and steep turn entries have focused instead on the use of the rudder for coordination. Airplane transfer function theory has been applied, as in the case just described for pitch maneuvers. As in Figure 10.10, pilot ratings are compared with parameters derived from the roll and sideslip due to aileron and rudder transfer functions (Hoh and Ashkenas, 1977). Rudder deflection is assumed to be used in a coordinated fashion to hold the sideslip angle to zero in abrupt aileron rolls, as pilots are trained to do. The essence of the Hoh and Ashkenas method is a solution for the precise rudder cross-feed that accomplishes this, using linearized transfer functions.

![Chapter 10 - Figure 1](../assets/chapter10/_page_10_Figure_1.jpeg)

**Figure 10.10** Required rudder cross-feed to coordinate turn entry, a significant factor for airplanes with good Dutch roll characteristics. The amount and sense of rudder required is plotted on the abscissa. The ordinate µ shows the required phasing of the rudder input. Rudder angle is sustained after initial input for positive values of µ and reversed for negative values of µ. The greatest pilot tolerance for required cross-feed occurs with µ = −1.0, for which cross-feed fades to zero after the turn is established. (From Hoh and Ashkenas, *Jour. of Aircraft*, Feb. 1977)

The solution is in two parts, magnitude and phasing. The phase dependence means that, depending on the detailsof the airplane'slateral-directional dynamics, the required rudder deflections for coordination, or cross-feed, may increase or decrease after the initial rudder application.

The end result of the analysis shows a strong favorable effect for a particular required rudder cross-feed phasing. Pilots tolerate the largest amount of rudder angle cross-feed for the case in which the required rudder angle tapers off toward zero as the turn is established. Conversely, if the required rudder angle cross-feed either increases beyond the initial value or changes sign during the turn, pilot ratings suffer and smaller cross-feed levels are tolerated.

The cross-feed phasing parameter µ that expressesall of thisisderived from the ratiosof the transfer function numerators of rudder to sideslip and aileron to sideslip. Excluding low (gravity) and high (direct force) frequency terms, the parameter µ expresses the separation between simple zeros in these numerators. Positive values of µ correspond to increasing rudder requirements during the turn and negative values to decreasing rudder requirements. The optimum case, in which the steady-state value in a turn goes to zero, corresponds to µ = −1.0.

#### **10.5 Supermaneuverability, High Angles of Attack**

Until the 1970s, fighter air-to-air combat followed the pattern set during World War I. Fighter pilotsmaneuver behind opposing fightersto bring fixed gunsto bear long enough for a burst. The tactics are much the same for narrow-field-of-view guided missiles, such as the AIM-9 Sidewinder. In the missile case, a tail position is held long enough for an acquisition tone; then the missile is launched.

Hawker-Siddeley in Britain came up with the thrust-vector–controlled Taildog missile concept in the late 1960s, making an off-boresight launch a possibility. Combined with a helmet-mounted sight, a Taildog-type missile can be launched at target airplanes at almost any position where the pilot can follow the target with his eyes. However, even with offboresight missile lockons and launches now possible, there is still interest in gunnery for air-to-air combat. Furthermore, there isinterest in gun bearing at high anglesof attack, increasing firing opportunities in a dogfight.

Supermaneuverability isdefined ascontrolled, or partially controlled, flight in the stalled regime. It takes two forms: first, a dynamic maneuver to a high angle of attack, beyond any equilibrium or trim point. Pitching angular momentum carriesthe airplane to a momentary peak angle of attack. The second form of supermaneuverability is flight to a sustainable trim equilibrium beyond the stall. Supermaneuverability is seen as a way to get into the tail chase position, by a feint, tricking a pursuing airplane into overrunning one's position. Supermaneuverability addsto a dogfighting airplane'soptions.

The Cobra maneuver, demonstrated with a Sukhoi Su-27 airplane by the Russian pilot Viktor Pugatchov at Le Bourget in 1989, isin the first category. After Pugatchov'sdemonstration in the Su-27, the same maneuver was performed in a MiG-29. The Cobra is started from unstalled flight with a rapid application of full nose-up control, which is held up to the maximum angle of attack point, about 90 degrees. Control is neutralized for the recovery, assuming that the airplane has a negative or nose-down pitching moment at that point.

The entire maneuver takes about 5 seconds. There is a small altitude gain but a huge loss in airspeed and kinetic energy. Ordinarily, during air combat, one tries to maximize airspeed and total (potential plus kinetic) energy as a reserve for further maneuvers. Thus, U.S. Major Michael A. Gerzanics, project test pilot for a vectored-thrust F-16, has stated that supermaneuverability is not beneficial in all tactical situations, but is rather something that he would like to have available for close combat with a strong adversary. Clearly, any uncontrolled yawing and rolling moments that develop in the 5-second period beyond the stall must be small. The Cobra maneuver has been elaborated with a sidewise variant, called the Hook.

#### **10.6 Unsteady Aerodynamics in the Supermaneuverability Regime**

Mathematical modeling in the supermaneuverability regime has to account for unsteady aerodynamic effects above the stall (Zagainov, 1993). Zagainov describes a state variable mathematical model, developed by M. G. Goman and A. N. Khrabrov, for coefficientssuch as *Cz* and *Cm*. The model has a first-order state equation that defines time dependence (Figure 10.11). The typical hysteresis loop found in forced oscillation tests into the stalled regime can be modeled in this way. Zagainov also discusses the strong rolling and yawing momentsthat appear in the angle of attack range where vorticesare shed from inboard strakes and extended forebodies. These vortex-generated rolling and yawing moments not only appear to exceed values measured in steady wind-tunnel tests, but they are also time-dependent, exhibiting hysteresis loops.

Additional light on the complex, unsteady air flows in the supermaneuverability regime has been shed by a combined wind-tunnel test and flow visualization program (Ericsson and Byers, 1997). A major factor is a coupling between vehicle motion and asymmetric cross-flow separation on a slender forebody. Wing leading-edge extensions or LEX, such as found on the F-16 and F-18 airplanes, change the nature of the cross-flow separation, apparently in a beneficial direction.

# **10.6.1** *The Transfer Function Model for Unsteady Flow*

Aerodynamicists familiar with the classical Bryan formulation of the perturbation equationsof airplane motion expect to find aerodynamic forcesand momentsexpanded in Taylor series. As an example, the yawing moment coefficient *Cn* isexpanded as *Cn* = *Cn*<sup>β</sup> × β + *Cnp* × pb/2V + *Cnr* × rb/2V + *Cn*<sup>δ</sup> × δ + ··· . The series uses the first derivative only of the function (*Cn*) with respect to the independent variables, which are the vehicle's state variables β, *p*, *r*, δ, etc. With thisbackground, it isnatural to treat unsteady flow effects by adding higher derivative terms to the expansion, such as *Cn*β˙ <sup>×</sup> <sup>β</sup>˙.

Although mathematically sound, thisapproach hasa seriousflaw (Greenwell, 1998). Numerical valuesof higher order derivativessuch as *Cn*β˙ can be correct at only one oscillation frequency. Numerical values obtained in oscillating wind-tunnel rigs are correct at the frequency tested, but are in general invalid for the free or controlled angular motions of an airplane.

The solution of this problem is readily apparent to engineers trained in servomechanism theory. That is, treat aerodynamic force and moment as the result of dynamic processes much ashydraulic actuatorsand electrical networksare treated. The transfer function concept shown in Figure 10.2 is ideal for this application. Other modeling methods, such as Fourier function analysis, can produce equally valid results, but as Greenwell points out, the transfer function approach has the great advantage of being easily integrated into flight simulation computer codes(Abzug, 1997). Greenwell further proposesparallel transfer functions for applicationsat anglesof attack that lead to separated flowsand vortex bursting, each with its characteristic model. Transfer functions are not limited to first-order lag forms, but these have dominated the field so far. A first-order lag form adds one additional state to a state space aerodynamic model, as in the Goman and Khrabov example of Figure 10.11.

![11.](../assets/chapter10/_page_13_Figure_1.jpeg)

![![](../assets/chapter10/_page_13_Figure_1.jpeg)](../assets/chapter10/_page_13_Figure_2.jpeg)

**Figure 10.11** Time-dependent mathematical model for aerodynamic force and momentsproposed by M. G. Goman and A. N. Khrabov for the fully stalled regime encountered in supermaneuvers. *Below*, lift coefficient variation with angle of attack, using this model. (From Zgainov, AIAA Paper 93-4737, 1993)

The transfer function concept applied to modeling unsteady aerodynamics in simulations istypical of many developmentsin that it isdifficult to establish priority. Greenwell credits Dr. Bernard Etkin asthe originator of the concept, with hispublication of a 1956 University of Toronto paper (UTIA Report 42). Early work on the concept also was done by Kenneth Rogers, Thomas Burkhart, J. Roy Richardson, Moti Karpel, William P. Rodden, and R. Vepa.

A 100-state aeroservoelastic model of the Grumman X-29A forward-swept wing research airplane uses the transfer function model for unsteady aerodynamics. The transfer function model was also used with success at the DLR to model lift hysteresis at the stall for the Fairchild/Dornier Do 328 (Fischenberg, 1999) (see Chapter 14, Sec. 8.4).

#### **10.7 The Inverse Problem**

A requisite for linear analysis is a reference motion about which small perturbations occur. Generating reference motions in the case of fighter airplane supermaneuvers can be a particular problem. A planar reference maneuver, such as a Cobra-type snapup, may be generated with no particular difficulty from flight path equations(short-period dynamics suppressed) for a specific airplane. One would apply full nose-up aerodynamic or thruster control until the desired peak attitude or angle of attack is reached, followed by full nosedown control. This open-loop maneuver would yield a time history of airspeed, attitude, and angle of attack from which operating points could be selected for small-perturbation stability analysis.

Difficulties can be expected only if a maneuver path in inertial space is specified, rather than an open-loop time sequence of control or thruster angles. In that case, an inverse solution isrequired to determine the airplane'svelocity along the path and to be sure that the maneuver is possible in the sense that control limits are not exceeded. Again, specifying a planar reference trajectory for inverse solution presents no difficulty. The case is different for nonplanar maneuversin that the geometry could become complex.

In principle, spatial sequences of six of the normal airframe states, the three position coordinatesof the center of body axesand the three Euler angles, can define any airplane maneuver. A natural path set of coordinates has been proposed instead, particularly for nonplanar maneuvers (Myers, McRuer, and Johnston, 1987). The method is illustrated with the familiar yo-yo tactical maneuver. Natural path coordinates– tangent, normal, and binormal – are a familiar concept in classical mechanics.

# **10.8 Thrust-Vector Control for Supermaneuvering**

While supermaneuvering flight maneuvers such as the Cobra can evidently be made with ordinary aerodynamic controls, there is a growing interest in thrust vectoring for supermaneuvering (Gal-Or and Baumann, 1993). Four recent thrust-vectoring flight demonstration programs are

- **F/A-18 HARV** (High Alpha Research Vehicle) Thrust is deflected by three vanes per engine for pitch and yaw control to a maximum angle of 12.5 degrees. Roll control is also available because of the airplane's two engines.
- **X-31** Thrust is deflected for pitch and yaw control to a maximum of 15 degrees by carbon paddles, integrated with the flight control system.
- **F-16D MATV** This airplane's thrust-vectoring system is integrated into the engine, with maximum yaw and pitch deflection anglesof 17 degrees(Figure 3.13).
- **YF-22 Prototype** Engine nozzlesare deflected in pitch at anglesof attack above 12 degreesand airspeedsunder 200 knots, blended with horizontal tail deflections. The airplane is controllable at an angle of attack of 60 degrees (Barham, 1994).

# **10.9 Forebody Controls for Supermaneuvering**

Alternativesto thrust-vector controlsat the high anglesof attack for supermaneuvering are the blowing or strake controls that act on the vortex systems shed by tactical airplanes' forebodies. There is an extensive literature on the effects of vortices shed by slender body noses on airplane forces and moments. The intent of blowing and strakes or

tabs is to modify these vortices for control purposes, particularly in the supermaneuvering high angle of attack regime.

Pedriero et al. (1998) demonstrated both the promise and problems of forebody blowing. Rolling and yawing moment coefficientsaslarge as0.02 and 0.4, respectively, are available with blowing to one side, for a cone-cylinder body with a 70-degree delta wing. However, moment linearity with jet mass flow is too poor for closed-loop control purposes. Adding controlled amounts of blowing to the opposite side improves linearity to the point where closed-loop control is possible, with no sacrifice in available control moment. In tests of forebody blowing for a model with a chine at the body'swidest point, control linearity with mass flow appears to be improved without resorting to blowing to the opposite side (Arena, Nelson, and Schiff, 1995).

The F/A-18 HARV was used to experiment with deflectable foldout strakes on the forward forebody for roll control at high angles of attack, with successful results (Chambers, 2000).

#### **10.10 Longitudinal Control for Recovery**

Tactical airplanesare able to reach supermaneuvering anglesof attack by low or even negative static longitudinal stability. Full nose-up control starts the pitchup; unstable or nose-up pitching moment keepsit going. Recovery requiresa nose-down pitching moment that will overcome the unstable pitching moment and leave a margin for nose-downward angular acceleration.

A rule of thumb for recovery nose-down pitching moment has been proposed, based on simulation studies and practical fighter design (Mangold, 1991). A pitching acceleration of 0.3 radians per second squared is said to be adequate. This leaves a margin for inertial coupling due to rolling during the pitching maneuver. A related problem isthe amount of longitudinal control power required for very unstable airplanes, not necessarily during supermaneuvers. For that problem, Mangold correlates required pitching acceleration control with time to double amplitude.

The recovery control problem also has been attacked using the classical Gilruth approach (Nguyen and Foster, 1990). Satisfactory and unsatisfactory recovery flight characteristics are used to draw a criterion line in a plot of minimum available pitching moment coefficients with full-down control versus a moment of inertia and airplane size parameter. With only five flight data points, Nguyen and Foster call their criterion preliminary.

### **10.11 Concluding Remarks**

Current tactical airplane maneuverability research spans all aspects of the stability and control field, from linearized transfer functions to unsteady aerodynamics and the complex, vortex-imbedded flowsfound at very high anglesof attack. Further advancesand new theories appear likely with the advent of thrust-vectoring and direct side and normal force control.