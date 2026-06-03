# *Flying Qualities Research Moves with the Times*

Robert R. Gilruth's key flying qualities contribution was to test a significant sample of airplanes for some flight characteristic such as lateral control power and then to separate the satisfactory and unsatisfactory cases by some parameter that could be calculated in an airplane's preliminary design stage. The Gilruth method put design for flying qualities on a rational basis, although Chapter 3 tells of some later backsliding, attempts to specify flying qualitiesparametersarbitrarily.

Modern timeshave brought the \$100 million and more airplane and development costs for new prototypesinto the billionsof dollars. Thishasmade for a scarcity of new machines that can be tested in the Gilruth manner and an interest in alternate flying qualities methods. The pilot-in-the-loop method surfaced around 1960 as an alternate way of rationalizing flying qualitiesand to focusattention on the pilot–aircraft combination asa closed-loop system. Pilot-in-the-loop analysis involves adoption of mathematical models for the human pilot as just another control system element.

The three basic concepts of the pilot-in-the-loop analysis method are (McRuer, 1973):

- 1. To accomplish guidance and control functions the human pilot sets up a variety of closed loops around the airplane, which, by itself, could not otherwise accomplish such tasks.
- 2. To be satisfactory, these closed loops must behave in a suitable fashion. As the adaptive meansto accomplish thisend, the pilot must make up for any dynamic deficienciesby adjustmentsof hisown dynamic properties.
- 3. There is a cost to this pilot adjustment: in workload stress, in concentration of the pilot'sfaculties, and in reduced potential for coping with the unexpected. The measure of the cost are pilot commentary and pilot rating, as well as physical and psychological measures.

In thischapter we trace the development of pilot-in-the-loop analysismethodsasthey apply to airplane flying qualities. Pilot-in-the-loop methods are clearly essential to study closed-loop operations such as tracking, but can they replace or add to the classical Gilruth approach?

# **21.1 Empirical Approaches to Pilot-Induced Oscillations**

Figure 21.1 is a time history of the pilot-induced oscillation that occurred during landing of the Space Shuttle Orbiter Enterprise in 1977. Pilot-induced oscillations (PIO), or airplane–pilot coupling (APC) incidents, in which pilot attempts at control create instability, are a natural subject for pilot-in-the-loop analysis and a major motivating factor for the method'sdevelopment. However, pilot-induced oscillationsappeared long before advanced pilot-in-the-loop methodswere in place. Engineerswere obliged to improvise solutions empirically, so that airplane programs could proceed.

One cause of pilot-induced oscillations was apparent without much deep study. If control surface rate of movement is restricted for any reason, such as insufficient hydraulic

![Chapter 21 - Figure 1](../assets/chapter21/_page_1_Figure_1.jpeg)

**Figure 21.1** Time history of pilot-induced oscillations that occurred during landing of the space shuttle Enterprise, on October 26, 1977. Time lags in the longitudinal control system are considered to have been the primary cause. (From Ashkenas, Hoh, and Teper, AIAA Paper 82-1607-CP, 1982)

fluid flow rate into actuation cylinders, the pilot is unable to reverse control motion quickly enough to stop an airplane motion, once started. A late correction drives the airplane too far in the reverse direction, requiring ever-increasing control motions. Describing function analysis of rate limiting does indeed show destabilizing phase lag. Thus, one empirical design rule for pilot-induced oscillation avoidance is high available control surface rates.

In unpublished correspondence W. H. Phillipscommentson other empirical findingson pilot-induced oscillations:

We found that very light control forces together with sensitive control were very likely to lead to pilot-induced oscillations. Viscous damping on the control stick was not the answer asthisput lag in the response to control force aswell asthe recovery. What wasneeded was a large force in phase with deflection for rapid stick movements, which could be allowed to wash out quite rapidly. This could be obtained with a spring and dashpot in series. Grumman called this a "sprashpot" and used it successfully in the feel system of the F-11F. . . . The negative *Ch*<sup>α</sup> of flap-type controlscausesthe control force to fall off after the airplane responds.

An additional empirical approach to solving longitudinal pilot-induced oscillation problems is the double bobweight system described in Chapter 5. An aft bobweight provides heavy stick forces to start a pitch maneuver, by applying pitching acceleration forces to the stick. Stick force falls off as the airplane responds.

### **21.2 Compensatory Operation and Model Categories**

Pilot-in-the-loop analysis methods have had their earliest and most meaningful successes representing compensatory operation. As applied to pilot-in-the-loop operation, in compensatory operation or tracking the pilot operates on displayed or perceived errors to minimize them in a closed-loop fashion. Precognitive pilot operation is essentially openloop; the pilot isnot part of the tracking loop.

Mathematical models for pilot compensatory operation fall into two categories, structural and algorithmic. Structural models reduce the pilot to subsystems such as muscle manipulators and vestibular sensors, each with transfer functions. Structural model pilot transfer functions contain delays, leads, and lags. The overall assemblage must reproduce pilot behavior in an end-to-end fashion. This challenging approach is made possible by careful frequency response measurements on human subjects (McRuer, 1973).

Pilot algorithmic modelshave grown out of modern optimal control theory. These models include an estimator, such as a Kalman filter, which processes the pilot's observations to provide an estimate of the airplane's state, and a controller, which is a mathematical model for the pilot'sregulation and muscular functions(Figure 21.2). Minimization or maximization of a criterion function provides the required results.

![2). Minimization or maximization of a criterion function provides the required r](../assets/chapter21/_page_2_Figure_6.jpeg)

**Figure 21.2** Algorithmic pilot model, used in an optimal control loop. The airplane or plant matrices A, B, C, and D, including a noise-shaping filter E, are at the upper left. The airplane's state is estimated by the Kalman-Bucy filter at the lower right. The optimal controller ison the lower left. (From Thompson, AIAA Paper 88-4183, 1988)

It isimportant to recognize that delay-lead-lag pilot modelsare needed primarily in analysis of compensatory operation of inner, generally attitude loops. Such loops are closed at high frequenciesrelative to pilot dynamics. Pure gain modelsfor the pilot are generally adequate for analysis of turn coordination and lower frequency speed and path control loops.

#### **21.3 Crossover Model**

The crossover model of compensatory operation grows out of the observation that pilots develop the necessary dynamics to produce in the pilot–airplane combination a particular transfer function in the crossover region of frequencies (McRuer, 1988). The pilot–airplane open-loop transfer function developed has the remarkably simple form of an integrated time delay, or ω*<sup>c</sup>* (*e*−<sup>τ</sup> *<sup>s</sup>*)/*s*, where the open-loop gain is ω*c*, τ isthe delay, and *s* isthe Laplace operator. The open-loop gain ω*<sup>c</sup>* iscalled the *crossover frequency*, the frequency at which the open-loop amplitude response crosses the 1.0- or 0-db line.

The closed-loop frequency response, or ratio of output to input for the crossover model, isflat at 1.0 at low frequencies, meaning that the output followsexactly the input. Asinput frequency israised, the frequency at which the output drops3 db lower than the input, or to only 70 percent of the input, is considered a cutoff for all practical purposes. This frequency defines the closed-loop system bandwidth. For the crossover model, the frequency that defines closed-loop system bandwidth is also the frequency ω*<sup>c</sup>* for which the open-loop system has a gain of 1.0.

The crossover model time delay τ isactually a low-frequency approximation, valid at crossover frequencies, for numerous pilot and control system delays and higher order lag terms. That part of τ due to the pilot becomesgreater asthe lead contributed by the pilot increases, a cost of additional pilot effort (McRuer, 1988). This reduces the available crossover frequency for other system lags.

# **21.4 Pilot Equalization with the Crossover Model**

All airplane transfer functions, such as the pitch response to elevator and the roll response to aileron, have first- or second-order denominator functions, arising from mass or inertia. To satisfy the crossover model the pilot must supply a canceling numerator function over the same frequency range. This amounts to lead or anticipation, agreeing with common sense as to what is required for the error elimination in compensatory operation.

The amount of lead or compensation required by the pilot is a direct measure of workload. The pilot lead is reflected in the positive slope of the pilot model amplitude ratio in the Bode diagram, in the vicinity of the crossover frequency. A large positive slope corresponds to excessive lead, high workload, and poor pilot rating. A numerical connection can be made between pilot rating by the Cooper-Harper scale, discussed in Chapter 3, and required lead equalization (Figure 21.3).

# **21.5 Algorithmic (Linear Optimal Control) Model**

The algorithmic or linear optimal control model ispartially a structural pilot model in that elementsof the optimal controller can be identified with the neuromuscular lag. However, the basic distinction between the algorithmic and structural pilot models is that, except for simple problems, the pilot cannot be represented with a simple transfer function in the algorithmic case. When very simple airplane dynamics (a pure integrator) are postulated in order to be able to generate a pilot transfer function, the linear optimal control pilot

![Chapter 21 - Figure 1](../assets/chapter21/_page_4_Figure_1.jpeg)

**Figure 21.3** Degradations (increases) in pilot rating for tracking tasks associated with degree of pilot lead required. (From McRuer, AGARDograph 188, 1974)

model is found to be of high order, but with characteristics similar to the crossover model (Thompson and McRuer, 1988).

The linear optimal pilot model hasbeen used to advantage in the generation of pilot ratings (Hess, 1976; Anderson and Schmidt, 1987), the analysis of multiaxis problems (McRuer and Schmidt, 1990), and the stability of the pilot–airplane combination in maneuvers (Stengel and Broussard, 1978).

# **21.6 The Crossover Model and Pilot-Induced Oscillations**

The crossover model has proved to be of great value in understanding pilot-induced oscillations. The way has been opened for validating empirical corrections for the phenomenon, such as described by Phillips, and for the development of new concepts in the area and superior flying qualities designs.

Duane McRuer provides a comprehensive survey of pilot-induced oscillations in a report for the Dryden Flight Research Center (McRuer, 1994). Having been experienced by the Wright brothers, pilot-induced oscillations qualify as the senior flying qualities problem. Recent dramatic flight experiences, combined with the availability of advanced analysis methods, have given the subject fresh interest. Between the years 1947 and 1994, there were over 30 very severe reported cases, in airplanes ranging from a NASA paraglider to the space shuttle Orbiter. McRuer proposes three pilot-induced oscillation categories, as follows:

essentially linear; quasi-linear, with surface rate or position limiting; essentially nonlinear, including pilot or mode transitions.

![Chapter 21 - Figure 1](../assets/chapter21/_page_5_Figure_1.jpeg)

**Figure 21.4** Pilot–airplane open-loop frequency responses for two configurations of the USAF/ Calspan variable-stability T-33. The upper case, with no pilot-induced oscillations, has the ideal integrator shape in the vicinity of crossover. The lower case, with severe pilot-induced oscillations, has a steeper slope and more phase lag at high frequencies. (From McRuer, STI Technical Rept. 2494-1, 1994)

An important validation of the crossover model approach to the first category was furnished by analysis of fully developed pilot-induced oscillations on the USAF/Calspan variable-stability NT-33 (Bjorkman, 1986). In six severe cases there were large effective open-loop system delays, departing from the ideal integrator-type airframe transfer function in the region of crossover (Figure 21.4). The required pilot dynamics for compensatory operation thusrequired

a great deal of pilot lead as well as exquisitely precise adjustment of pilot equalization and gain to approximate the crossover law and to close the loop in a stable manner.

Linear pilot-induced oscillationsinclude complex interactionswith airplane flexible modes. Mode-coupled oscillations have been experienced on the F-111, the YF-12, and the Rutan Voyager. Control surface rate-limiting pilot-induced oscillations were discussed previously.

Essentially nonlinear pilot-induced oscillations have arisen chiefly in connection with pilot and mode transitions. In one such case, weight-on-wheel and tail strike switches changed the stability augmentation control laws on the Vought/NASA fly-by-wire F-8, presenting the pilot with a rapid succession of different dynamics (McRuer, 1994). The pilot was unable to adapt in time. Mode transitions, either as a function of pilot input amplitude or automatic mode changes, are a particular source of pilot-induced oscillations in modern fly-by-wire flight control systems. The importance of avoiding pilot-induced oscillations on fly-by-wire transport airplanes led to the study discussed in Sec. 11.

#### **21.7 Gibson Approach**

In his 1999 thesis at TU Delft, John C. Gibson proposes a different categorization of PIO from that of McRuer (Sec. 6). In one category are PIOsthat arise from conventional loworder response dynamics. The pilot can back out of these by reducing gain or abandoning the task. In thiscategory the lag in angular acceleration following a control input isinsignificant, giving the pilot an intimate linkage to the aircraft response.

In the second category are PIOs arising from high-order dynamics in which the pilot is locked in and isunable to back out. High-order dynamicssuch asexcessive linear control law lagsor actuator rate and/or acceleration limiting create large lagsin acceleration response, disconnecting the pilot from the response.

In the first category, solutions can be developed assuming only the simplest of pilot models. The basic idea is that fly-by-wire technology can be used to shape the response so that the control laws provide the McRuer crossover model for the airplane–pilot combination, with the pilot required only to provide simple gains. Of course, other factors such as sensitivity, attitude and flight path dynamics, and mode transitions must be considered.

The second category, involving high-order dynamics, requires detailed examination of the evidence to define the limit of high-order effects that can be tolerated. Stop-to-stop stick inputsat critical frequenciesmust be evaluated.

# **21.8 Neal-Smith Approach**

The connection between excessive lead requirements for control and poor pilot ratingsisthe basisfor the Neal-Smith criterion, dating from 1970. A lead-lag pilot model is assumed, with a fixed time delay of 0.3 second. When this pilot model is combined with the dynamicsof the airplane, the model parameterscan be adjusted to meet bandwidth and other closed-loop requirements. The resultant pilot model phase lead and closed-loop resonance are compared with pilot opinions to establish acceptable boundaries (Figure 21.5).

The Neal-Smith approach isan important contribution to the rationalization of flying qualitiesrequirementssince it makesdirect use of the mathematical pilot model. The method hasshortcomingsin that the required pilot lead isstrongly dependent on the required bandwidth, an arbitrary starting point (Moorhouse, 1982).

![Chapter 21 - Figure 1](../assets/chapter21/_page_7_Figure_1.jpeg)

**Figure 21.5** Neal-Smith criterion for pitch control. Acceptable short-period behavior occurs below the boundary established by closed-loop peak resonance ratio, the abscissa, and pilot model lead, the ordinate. The hatched boundaries are more restrictive limits proposed for large transports. (From Mooij, AGARD LS-157, 1988)

# **21.9 Bandwidth-Phase Delay Criteria**

The insights furnished by the crossover model for compensatory operation lead to criteria that can be used in control system design, as in the Neal-Smith approach. An important example isthe Hoh-Mitchell-Ashkenasbandwidth and phase delay criteria (Hoh, 1988), a combination of two individual metrics, illustrated in Figure 21.6.

The first metric is *aircraft* bandwidth, defined asthe frequency at which the phase angle of attitude response to stick force input is −135 degrees. The aircraft bandwidth measures the frequency over which the pilot can control without the need for lead compensation. The second metric is phase delay, defined as the difference in response phase angle at twice the frequency for a −180-degree phase angle and 180 degrees, divided by twice the frequency for a −180-degree phase angle. The phase delay metric approximates the phase characteristics of the effective airplane dynamics, from the region of crossover to that for potential pilot-induced oscillations. Systems with large phase delays are prone to such oscillations.

Boundaries in aircraft bandwidth–phase delay space have been developed using flight and simulator pilot ratings and commentary. Similar boundaries have been especially useful for rotorcraft and special (translatory) modes of control. With these boundaries, designers are able to account for closed-loop pilot–airplane dynamics, using effective airplane dynamics alone. A related airplane-alone criterion based on the crossover model is the Smith-Geddes (1979) criterion frequency. Still another criterion based on airplane-alone dynamics places boundaries in the Nichols plane of the attitude frequency response (Gibson, 1995). The idea is to confine the attitude frequency response within boundaries defined by the best piloted closed-loop flying qualities. All of these boundary methods depend on simple correlation. They should be effective to the extent that new cases resemble those on which the boundaries are based.

![Chapter 21 - Figure 1](../assets/chapter21/_page_8_Figure_1.jpeg)

- 
- 

**Figure 21.6** Definitionsof the bandwidth and phase delay criteria. (From MIL-STD-1797A, 1990)

Good design practice suggests using all of these criteria to examine airplane dynamics at issue.

# **21.10 Landing Approach and Turn Studies**

There isa large classof advanced flying qualitiesstudiesthat hasbenefitted from modern pilot-in-the-loop technology without requiring delay-lead-lag mathematical models for the pilot. For loop closures made at frequencies of 1.0 radian per second or lower, simple gain modelsfor the pilot appear adequate. Low-frequency closed loopscharacterize airspeed and path control outer loops.

STOL (short takeoff and landing) flight path control loops are the outer loops around higher frequency pitch attitude inner loops. The path loops can be closed with simple pilot gains, assuming tight control of the inner loop (Ashkenas, 1988). Where some modest pilot lead isrequired to achieve the ideal integrator-type pilot–airplane transfer function in the crossover region, pilot ratings will be degraded.

Wings-level turn and turn coordination studies fall into the same category of lowfrequency closed loops for which simple gain pilot models are adequate. The Ashkenas-Durand reversal parameter and the Heffley closed-loop studies of the naval carrier approach problem (Chapter 12) are yet additional examples of the use of simple pilot gain models.

#### **21.11 Implications for Modern Transport Airplanes**

Historically, pilot-induced oscillations (PIO) associated with fly-by-wire technology have occurred in military and experimental aircraft, which usually introduce advanced technologiesbefore they appear on civil transports. Thishasprovided a breathing space for that category of PIO problemsto be worked out before exposing the traveling public to new hazards. However, fly-by-wire technology is now standard for new transport airplanes, bringing the possibility of PIO.

A U.S. National Research Council (NRC) report (McRuer, 1997) is intended to alert all interested parties to this hazard and to offer recommendations to avert serious problems in the future. Aside from the evident need to continue research and pilot training in this area, a few striking conclusions and recommendations emerge from the NRC report:

- 1. Parameters measured by on-board flight recorders, the "black boxes," need to be at higher data rates, to capture PIO events that may have contributed to accidents. Dr. Irving Statler, who isinvolved in a major part of NASA'sAviation Safety Program, statesthat the highest data rate found in black box recordersisonly 8 samples per second, as compared with the 20–30 samples per second needed to capture PIO events.
- 2. Highly demanding tasks with known and suspected triggering events for PIO should be included in simulation, flight test, and certification. These tests should use pilots with experience and training in PIO events.
- 3. Current certification procedures should be revised to incorporate existing techniquesfor mitigating the risk of PIO.

The warningsthat were sounded by the NRC report of potentially dangerousPIOsin commercial aviation should be taken seriously. The recommendations of the experienced group that wrote the report should be put into action.

On the matter of recording PIO eventsthat may have contributed to accidents, an ambitiousapproach isunder study at the Aerospace Corporation and at RTCA (Grey, 2000). This is a satellite-based aircraft monitoring system and data archive that does away with the need for on-board flight recorders. The satellite-based system could provide real-time, high-data-rate information for accident prevention or diagnosis. Such a system is seen as a logical outgrowth of developmentsin the field of communications.

# **21.12 Concluding Remarks**

Pilot-in-the-loop studies are partially in the realm of traditional scientific research and partially one of the technologiesbelonging to airplane stability and control. Aspure research, one exploresthe interesting interactionsof human beingsand machinesperforming various flying tasks. With pilot and crew error said to be responsible for a large number of accidents, there is a strong motivation for support of this research enterprise.

To date, clear successes of pilot-in-the-loop studies as technology are the applications of the crossover and linear optimal models to explaining and avoiding a large group of pilot-induced oscillations. The crossover model has also been the foundation for metrics used in specifying flying qualities. Other accomplishments, such as better understanding of pilot loop closuresin STOL and carrier approachesand in turn coordination, have relied on normal bandwidth-maximizing closed-loop design techniques, with the pilot represented asa simple gain. Pilot-in-the-loop methodshave thusappeared asthe next step following the classical flying qualities work, which emphasized control power and suitable control forces.

A potential for dangerouspilot–airplane interactionsin advanced commercial transport airplaneshasbeen uncovered. A well-considered plan to mitigate these problemsshould be put into action.