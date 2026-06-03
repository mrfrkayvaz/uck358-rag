# *Stability Augmentation*

Stability augmentation isthe artificial improvement, generally by electromechanical feedback systems, of airplane stability and control *while the airplane remains under the control of the human pilot*. Stability augmentation generally changesthe airplane'sstability derivativesand modesof motion.

We make the important distinction between stability augmentation, artificial feel systems, and airplane automatic pilots. While artificial feel systems, discussed in Chapter 5, may alter stick-free stability for the better, their main function is providing manageable control forces. Automatic pilots replace the human pilot when they are in use.

#### **20.1 The Essence of Stability Augmentation**

To be a true stability augmenter, the device must change the airplane's flight characteristicswithout the pilot'sperception. Thismeansthat augmenter outputsmust add to those of the pilot in a series fashion. Augmenter outputs put into the primary control circuit between the cockpit and the control surfaces must move only the control surfaces, and not the cockpit controls. The requirement to not move the pilot'scontrolsissidestepped if the augmenter isnot inserted into the primary control circuit but movesa separate, or dedicated, control surface. Still another way around the need for augmenters not to move the pilot'scontrolsisthe integrated control surface actuator (Chapter 5), used in fly-bywire control systems. Integrated servo actuators accept and add electrical signals from both cockpit controls and stability augmenters.

In fly-by-cable control systems, isolation of primary-control-circuit stability augmenter outputs from the cockpit controls is a surprisingly difficult mechanical design problem. Control valve friction in control surface actuatorsactsto hold the surfacesfixed for small stability augmenter signals. When this happens, the augmenter in effect backs up and moves the cockpit controls instead. The result is an unaugmented airplane for small disturbances and limit cycle oscillations, such as yaw snaking. One cure for excessive valve friction can be asbad asthe small signal backup problem. Thisisto center the cockpit controlswith husky spring detents, which have to be overcome by the pilot in normal control use.

The degree of authority of stability augmentation systems is another important design consideration. Since augmenters operate ideally without moving the pilot's controls, the pilot will be unaware of abrupt failuresto the limit of augmenter authority until the airplane reacts. Then, there should be enough pilot control authority left to add to and cancel the failed augmenter inputs, with something to spare. This was the design philosophy until the advent of redundant, self-correcting augmentation systems, which make feasible augmentation at full authority or control surface travel.

Automatic pilots, which replace the human pilot when they are in use, are expected to move the cockpit controls. Abrupt full autopilot failures are instantly apparent to an attentive flight crew. Larger control authority than for stability augmenters is feasible, even for systems without the redundant, self-correcting feature.

#### **20.2 Automatic Pilots in History**

Stability augmentation goesback only to about 1945, while the history of airplane and missile automatic pilots, or autopilots (that word happens to be a trademark of a particular manufacturer), actually beginsbefore the Wright brothers, with Sir Hiram Maxim's 1891 designs. That history has been told by several authors, including Bollay (1951) and the scholarly but very readable account of automatic pilot development in the first chapter of *Aircraft Dynamics and Automatic Control* by McRuer, Ashkenas, and Graham, dated 1973.

An additional historical account of airplane automatic pilots is that of W. Hewitt Phillips, in his Dryden Lecture in Research (1989). All of these authors refer to the remarkable 1913– 1914 demonstration of the Sperry "stabilizer," which provided full automatic control of a Curtiss Flying Boat. However, the present chapter deals only with stability augmentation.

Gust-alleviation systems are a specialized form of airplane automatic pilots, designed to reduce structural loads and to improve ride quality in rough air. These systems are of less interest now than formerly because modern airplanes can fly above turbulence or use weather radar to avoid storms. A complete historical review of gust-alleviation systems is available in a NASA Monograph (Phillips, 1998).

#### **20.3 The Systems Concept**

The concept of the airplane'sairframe asonly one object in a complete dynamical system is part of the thinking of today's stability and control engineer, when faced with the need for stability augmentation. Yet, early researchers in airplane stability augmentation did not approach the problem that way (Imlay, 1940). Imlay enlarged on the classical Routh criterion for stability by the use of equivalent airplane stability derivatives. The equivalent derivativesare the basic control-fixed stability derivativesplusthe productsof control derivativessuch asthe yawing moment coefficient due to rudder deflection and a gearing ratio. The gearing ratio is an assumed control deflection per unit airplane motion variable. For example, Imlay studied gearingsof 0.356 and 1.116 degreesof rudder angle per degree of bank and yaw, respectively.

The point isthat the Imlay stability augmentation analysismethod dealsonly with a modified airplane. No other dynamical elementsare represented, although the lag effects of the servomechanism that would drive the control surfaces are suggested by a somewhat awkward representation of a simple time lag as the first three terms of the power series for the exponential.

The key mathematical concept that leadsto modern augmentation analysismethodsis the control element, which isrepresented graphically by a box having an input and an output. Control element boxesare linked one to another, with the output of one serving asthe input to another. Control elements include sensors such as gyros; pneumatic, electric, or hydraulic control actuators; and, of course, the dynamics of the airframe, or control surface angle as an input and motion such aspitch or yaw rate asan output. Summing and differencing junctionsact on inputsand outputsasneeded, most notably to create an error signal. This is the difference between the commanded and actual system outputs.

### **20.4 Frequency Methods of Analysis**

Frequency methods of analysis ushered in the age of modern airplane stability augmentation and autopilot analysis. In his 1950 Wright Brothers Lecture, Dr. William Bollay reminded us that the application of frequency-response methods to the airplane case came a full ten years after their use in the development of anti-aircraft gun directors. The footprints of the electrical engineering community in this field are still evident in the use of terms such as decibels and octaves in some airplane frequency-response studies.

Frequency response is the steady-state sinusoidal airplane motion perturbation in response to steady-state sinusoidal control surface input perturbation. Only the amplitude ratio and phase relationship of the two sinusoids are of interest. Frequency response of mechanical and electrical devicesisreadily found from the parametersof the linearized differential equationsthat describe the device'smotion or electrical properties. The formal mathematicsthat do thisrest on the Laplace transformation, asexplained in Chapters3 and 4 of the classic 1948 text *Principles of Servomechanisms*, by Gordon S. Brown and Donald P. Campbell.

Frequency-response analysis led stability and control engineers to an entirely new way to describe airplane dynamics, the transfer function. The transfer function is the mathematical operator by which any input function ismultiplied to obtain the output function for that element. Transfer functions are numerical or literal expressions in the Laplace variable *s*. Transfer-function denominators are nothing but the characteristic equation, with Routh's and Bryan'soperator λ replaced by the complex Laplace variable *s*. Transfer-function numerators are governed by the input. Thus, the classical transfer function that converts elevator angle disturbances to pitch attitude disturbances is a second-degree polynomial in *s* divided by a fourth-degree polynomial in the variable *s*.

One of the first known applications of frequency response in airplane stability augmenter design was made by Roland J. White for the XB-47 yaw damper. White used the inverse frequency-response diagrams described by H. T. Marcy in 1946, in an electrical engineering context. Over the years, frequency-response analysis has never gone out of fashion. For example, the demanding X-29A flight control system was designed using Bode frequency plot techniquesby Grumman engineersled by Arnold Whitaker, JamesChin, Howard L. Berman, and Robert Klein.

Frequency-response methods are used in some of the latest airplane flight control design methods, giving frequency response another lease on life. As detailed in a later section, singular value methods, associated with robust control theory, use frequency response.

### **20.5 Early Experiments in Stability Augmentation**

The first stability augmenters appeared during World War II. Little detailed information isavailable about them. A German Blohm and VossBv 222 flying boat was thought to have had a pitch damper acting through a small, separate elevator surface. In a paper delivered in 1947, M. B. Morgan described an experimental yaw damper installed on a Gloster Meteor jet airplane. Other notable early designs were the Boeing B-47 and the Northrop YB-49 yaw dampers and the Northrop F-89 sideslip stability augmenter, which are discussed below.

### **20.5.1** *The Boeing B-47 Yaw Damper*

The B-47 Stratojet wasa radical airplane in itstime, a six-jet bomber with very flexible sweptback wings. Early flight tests disclosed that damping in yaw at low airspeeds wasmuch lessthan pilotscould deal with in landing approaches. The main pilot objection wasto the rolling portion of the motion, caused by the dihedral effect of the swept wingsat high angles of attack. After discarding other alternatives, Boeing engineers decided to attack the rolling motion indirectly, by artificial yaw damping using a rate gyro and the airplane's rudder. That is, by suppressing side-slipping motions, the airplane's rolling moment due to sideslip would not cause the objectionable wallowing in landing approaches.

The engineers who were chiefly responsible for the XB-47 yaw damper design were William H. Cook and Edward Pfafman. Roland J. White, who made a frequency-response analysis of the XB-47 yaw damper design, provides a complete account of the development (White, 1950)*.* In White'saccount one can find all of the elementsthat go into modern stability augmenter designs, even though in unfamiliar form in some cases. These are

the application of servomechanism analysis, using the equations of airplane motion;

airframe mathematical model includes aeroelastic bending effects;

irreversible power controls;

stability augmentation series servo, isolating the pilot from the servo action; artificial feel system.

Roland White's XB-47 yaw damper servomechanism analysis, using inverse frequency response, was advanced for its time. However, the all-important matter of loop gain, or commanded rudder angle per unit yaw rate, was apparently settled in flight test. William Cook remembers that Robert Robbins, the XB-47 test pilot, had a rheostat that varied yaw damper gain, and that Robbins chose the value that seemed to work best.

With no fund of stability augmenter design information to draw upon, Cook and Pfafman improvised the yaw damper both in terms of design requirements and hardware. A short phone call from Cook at the Moses Lake flight test site to Pfafman laid out the key design requirementsof rudder damping authority (one-fourth of full travel) and seriesactuation. The yaw damper servo was an electric motor and amplifier that had been used for B-29 turbo-supercharger waste gate control (Figure 20.1).

White's paper was delivered at the Design Session of the Institute of the Aeronautical Sciences1949 Annual Summer Meeting in LosAngeles. The concept of stability augmentation as a normal design feature for swept-wing airplanes had not yet been established, and White's paper irritated at least one purist. According to Duane McRuer, this person, a respected professor of design at Cal Tech, got off the following comment during the paper's discussion period:

If the B-47 had been designed properly, it would not have needed electronic stability augmentation.

William H. Cook (1991) reports a similar reaction from an MIT professor, unhappy that an "artificial" solution had been used on the B-47 to solve an aerodynamic stability problem. Of course, there is a perfectly sound aerodynamic reason why yaw stability augmentation isneeded on jet airplanesand isnot an evidence of poor design. Approximately, Dutch roll damping ratio is directly proportional to atmospheric density. An airplane with a satisfactory damping ratio of 0.3 at sea level will have a damping ratio of only 0.06 at an altitude of 45,000 feet.

### **20.5.2** *The Northrop YB-49 Yaw Damper*

The Northrop YB-49 shares with the Boeing B-47 the distinction of being one of the first stability-augmented airplanes in the modern sense (Figure 20.2). Duane T. McRuer (1950) described the YB-49'syaw damper asfollows:

![2). Duane T. McRuer (1950) described the YB-49'syaw damper asfollows:](../assets/chapter20/_page_4_Picture_1.jpeg)

**Figure 20.1** The series-type actuator (a surplus turbo waste gate servo) used in the Boeing XB-47 Stratojet'srudder push rod, to provide yaw damping. (From White, *Jour. of the Aeronautical Sciences*, 1950)

For the sensing part of the system, a Honeywell Autopilot rate gyro was chosen. . . . An electrical signal isthen produced which isproportional to thisspeed or yaw rate. This signal is fed back through an electrical amplifier and reversible motor. Here the signal is transferred mechanically to a linkage that actuates the rudder cable system. The heavy work, that of opening the clamshell rudder to drag the wing back in line, then falls to the fully-powered rudder hydraulic system.

McRuer since added to this description the information that the reversible motor that put a yaw damping input in series with pilot's inputs was a turbo-supercharger waste gate servo, asfor the B-47. The long cable that runsfrom the cockpit to the hydraulic servo valveson the clamshell rudders was expected to serve as a backup for the series-installed yaw damper servos. Unfortunately, initial yaw damper actuator motions stretched the cables until the hydraulic servo valve friction wasovercome. Thiscreated a dead spot until corrected by a reduction in hydraulic valve friction.

McRuer and Richard J. Kulda made the preliminary stability analysis by the method of equivalent stability derivatives, used in the literal approximate factors for the spiral and Dutch roll modes. The detailed design used Bode and Nyquist diagrams, much as in the case of the B-47. The YB-49's yaw damper had no washout to cancel the yaw rate signal in steady turns. Compared with current practice, the five weeks or so that it took to design, round up parts, install, and check out the YB-49's yaw damper is of course quite short.

![Chapter 20 - Figure 1](../assets/chapter20/_page_5_Figure_1.jpeg)

**Figure 20.2** The outboard flaps on the Northrop YB-49 are split at the trailing edge to act as rudders. They provide yawing moments for the airplane's series-type yaw damper. The YB-49 and Boeing XB-47 were the first airplanes with series-type yaw dampers. (From Ashkenas and Klyde, NASA CR 181806, 1989)

### **20.5.3** *The Northrop F-89 Sideslip Stability Augmenter*

The straight-wing twin-jet F-89 was originally flown with a conventional rate gyro yaw damper, with washout for steady turns. The rate gyro was replaced with a sideslip sensor, to reduce adverse (top) rudder angle in lead pursuit courses more than the yaw rate washout could do. The F-89 sideslip stability augmenter improved directional stability as well asDutch roll damping.

### **20.6 Root Locus Methods of Analysis**

One of the remarkable stories in the stability and control field is the invention of the root locus analysis method by Walter R. Evans. This came relatively late in the game for a fundamental advance in control system analysis. The root locus method first appeared in Evans' Master's degree thesis at the University of California, Los Angeles, followed by a North American Aviation report. The first root locus journal paper (Evans, 1948) waspublished over objectionsfrom refereeswho thought the work wasof little merit. While the method isknown simply asthe root locusmethod in the United States, Russian papers quite properly call it the Evans method. The root locus method received wide publicity with Dr. William Bollay's1950 Wright BrothersLecture, but even before the 1948 journal publication it had "spread like wildfire," according to Duane McRuer. Thishappened because John Moore at UCLA and Phillip Whittaker at MIT lectured on the method, using drafts of the North American report.

The essence of the root locus method is the set of rules that Evans discovered for the migration of roots of an open-loop system to the roots of the same system when the loop is closed. Airframe open-loop roots are nothing more than the airframe roots discussed by G. H. Bryan in 1911, the short- and long-period airplane modes of motion, and the aperiodic modes such as the spiral and roll modes. Evans found that the open-loop modes migrate toward the open-loop zerosasclosed-loop gain isincreased from zero (the open-loop case) to infinity. The open-loop zerosare the rootsof the numerator function of each element's transfer function.

Root locusmethodssurvived from the 1950sto the present day asone of the most widespread flight control system analysis and synthesis methods. Modern variants are

- *<sup>z</sup>***-Plane** The *<sup>z</sup>*-plane root locusmakesuse of the *<sup>z</sup>*-transform, where *<sup>z</sup>* <sup>=</sup> *<sup>e</sup>T s* and *s* isthe Laplace transform variable (Bollay, 1951). The complex number *z* is defined only at the switching or sampling times *T* of a sampled-data or digital control system. Since the states of sampled-data or digital control systems are likewise defined only at sampling times *T* , the *z*-plane root locuscan be used for stability and performance analysis of these systems. In the *z*-plane, real partsof the variable *z* are plotted along the abscissa, while imaginary parts are plotted along the ordinate. The Evans *s*-plane root locusrulesapply aswell in the *z*-plane. Only the region of stability and lines of constant damping ratio differ.
- *w* **and** *w* **-Planes** An improved transformation method for dealing with sampled-data or digital systems appeared in the 1950s, called the *w*-plane. The complex variable*w*iscreated by a bilinear transformation on *z*, or*w*= (*z*−1)/(*z*+1). Richard F. Whitbeck and L. G. Hofmann (1978) describe a scaled version of the *w*-domain with even better properties. Thisisthe *w* -domain, in which *w* = 2*w*/*T*. In contrast to the *z*-plane, the left or stable half of the*w* -plane corresponds to the left or stable half of the *s*-plane. Powerful analogiesexist between the *s*- and *w* -domains, allowing use of conventional root locus and Bode (Bollay, 1951) design tools. As a drawback, *w* transfer functions are far more complex algebraically than *s* transfer functions.
- **Unified Analysis Using Bode Root Locus** The Bode root locusisa hybrid method developed by Duane McRuer (McRuer, Ashkenas, and Graham, 1973) that addsto the conventional Bode plot the amplitude ratiosof the various loci in the *s*-plane. For any given loop gain actual closed-loop roots, all of the conventional frequency response quantities and the sensitivity to gain changes are seen in this plot.
- **Root Locus Sensitivity Vectors** Sensitivity vectors can be drawn from unaugmented airplane poles, such as the Dutch roll complex conjugate pair, giving the directionsand magnitude in the complex plane of the migration of those poles for individual feedbacks. The effects on a Dutch roll mode of unconventional feedbacks, such as sideslip and lateral acceleration to the ailerons, can be compared. Root locus sensitivity vectors were first published by Duane McRuer and Robert Stapleford (1963).

#### **20.7 Transfer-Function Numerators**

Airplane transfer-function denominator factors, or roots, govern airplane motions following initial disturbances. Stable roots, having negative real parts, lead to subsidence of oscillatory or aperiodic motions. The same is true for the denominators of closed-loop transfer functions, and early root locus work, such as the material in Dr. William Bollay's 1950 Wright Brothers Lecture, dealt with roots, or poles, of the closed-loop denominator. Transfer function numerator factors are called zeros. A response survey to step inputs for a systematic variation in pole–zero combinations (Elgerd and Stephens, 1959) gives striking results, particularly for the case of two real poles and one real zero. Depending on whether the zero is between the poles or to the right, the step response appears either deadbeat or with a large overshoot.

Transfer-function zeros play an important role in the closed-loop responses of stabilityaugmentation systems. The details are too involved to go into here, but some examples can be touched upon. In the altitude or glide path loop in which errorsare corrected by elevator or stabilizer control, a zero called 1/*Th*<sup>1</sup> can be in the right half of the root locus plane. This occurs on the back side of the power required curve, or at airspeeds below the minimum drag point. Loop closure drives a closed-loop real root into the right half-plane, with consequent divergence. An inner stability augmentation loop can correct this.

Another example is the complex zero associated with bank angle control by the ailerons. The Systems Technology, Inc., symbol for the undamped natural frequency associated with thiszero is ωφ. For valuesof ωφ that exceed the Dutch roll undamped natural frequency ω*<sup>d</sup>* , loop closure excites the Dutch roll and closed-loop stability is degraded. A complete tutorial discussion of this problem, as well as the altitude control zero problem, is given by Duane T. McRuer and Donald E. Johnston (1975).

## **20.8 Transfer-Function Dipoles**

The problem of the complex zero in the bank angle–aileron transfer function happens to be one of a class of transfer-function dipole problems in stability-augmenter design. In many lightly damped airplane modes, the root in question is near a complex zero. The pole–zero pair iscalled a dipole. Root locusrulesgenerally make sure that, for the pair, the locusthat originatesat the pole endsat the zero, forming a semicircle along the way.

When the dipole is close to the root locus imaginary axis, the semicircle can pass into the unstable, or right-half, plane. Conversely, by assuring that the semicircle forms to the left, closing the loop increases the stability of that lightly damped mode. This is called phase stabilization. By far the most important application of phase stabilization is to the bending and torsional modes of an elastic airplane with stability augmentation. As in the case of the bank angle transfer function, the modes are phase-stabilized when the dipole zero has a lower undamped natural frequency than the pole, or root.

### **20.9 Command Augmentation Systems**

Command augmentation systems, or CAS, are a relatively recent form of airplane stability augmentation. Pilot control inputs, usually filtered or shaped, are compared with measured airplane motions, with the differences being sent to the control surface actuation servos (Figure 20.3). In early command augmentation applications, such as in theMcDonnell Douglas F-4, F-15, and F-18 and the Rockwell B-1, the augmentation system has limited authority. There are parallel direct links from the sticks to the control surface servos.

![Chapter 20 - Figure 1](../assets/chapter20/_page_8_Figure_1.jpeg)

**Figure 20.3** Block diagram for the lateral-directional command augmentation system for the X-29A research airplane. Key features are the rate-limiters on roll and yaw commands. These minimize the possibility of rate-limiting the control servos due to large pilot control inputs. (From Clarke, Burken, Bosworth, and Bauer, NASA TM 4598, 1994)

The command augmentation systems of later airplanes such as the fly-by-wire General DynamicsF-16 have full-authority and high-command gains. Full-authority roll command augmentation systems have worked very well, with sharp, rapid, and precise responses to control inputs (Mitchell and Hoh, 1984). Some problems come along with these successes. Oversensitivity to small inputs, overcontrol with large inputs, and the phenomenon called roll-ratcheting can occur.

### **20.9.1** *Roll-Ratcheting*

Roll-ratcheting bearsa resemblance to the aileron buffeting that occurson sharpnosed Frise ailerons. The limit cycle oscillations occur at about 3 cycles per second when the aileronsare hard over, and the flight recordseven look the same (compare Figure 20.4 with Figure 5.6). However, the two phenomena could hardly be more different.

Roll-ratcheting arises from interactions among a variety of mechanisms. These include arm neuromuscular effects, limb and stick mass effective stick bobweights, force-sensing side stick gains, and roll command prefiltering. At 2 to 3 cycles per second, pilot voluntary effortsare not involved, so that roll-ratcheting isnot a form of the pilot-induced oscillations discussed in Chapter 21.

A major effort was made to pin down roll-ratcheting parameters, using a fixed based simulator (Johnston and McRuer, 1977). The progress of that investigation, which brought in flight test data from the NT-33 variable-stability research airplane as well as the F-16, is given in fascinating detail by Irving L. Ashkenas in a summary paper (1988). There is a convincing correlation involving the stick sensing force gradient (degrees per second of roll rate per pound of stick force) and roll time constant *TR*, in seconds. A single line divides roll command augmentation systems into ratcheting and nonratcheting cases. However, this particular correlation is thought to hold only for nonmoving or force-type side sticks, such asinstalled in the F-16 airplane.

The role of arm neuromuscular effectsasa prime component of roll-ratcheting isquestioned by Gibson (1999). In Delft TU studies, a simple assumption of a lateral bobweight

![Chapter 20 - Figure 1](../assets/chapter20/_page_9_Figure_1.jpeg)

**Figure 20.4** Flight record of roll ratcheting during banking maneuvers. (From Mitchell and Hoh, *Jour. of Guidance*, 1984)

loop wasfound to produce roll-ratcheting. A later paper from DVL, Braunschweig (Koehler, 1999) returns to the neuromuscular model with refinements, adding torso and hip dynamics to that of the arm. The Koehler paper claimsgood correlation with an F-16 XL roll-ratcheting incident. Gibson notes that a spectacular roll-racheting incident involving the F-18 is described by Klyde (1995). A mild rachet occurred on the BAe FBW (fly-by-wire) Jaguar airplane, which wascured by adding a stick damper and by changesto high-frequency control dynamics.

A prudent design approach to avoid roll-ratcheting might be to adhere initially to the Ashkenas 1988 force gradient/roll time constant criterion, supplementing this with detailed stability analyses that account for both neuromuscular and bobweight effects.

### **20.10 Superaugmentation, or Augmentation for Unstable Airplanes**

The design goal of classical stability augmentation, such as in the XB-47 and YB-49, isto merely restore acceptable flying qualitiessuch aswell-damped Dutch roll or pitching oscillations to airplanes that have poor characteristics. The loss is usually due to operation at high altitudes, or at low speeds with airplanes designed for high speeds.

With the success of classical stability augmentation designers have become bold. They now offer the prospect of significant flight performance gains by flying unstable airframes. Superaugmentation makes inherently unstable airplanes have stable flight characteristics while retaining the performance gains. The greatest performance gains appear possible for airplanesinherently unstable in pitch. According to Peter Mangold, maximum lift coefficient increases of 25 percent and trim drag decreases of 20 percent can be obtained with a longitudinally unstable tailless design as compared with its stable counterpart. These large improvements arise from the down-trailing-edge angles required to trim an unstable flying wing, increasing wing camber. A negative camber is required to trim a stable flying wing. More modest gains are available for tailed airplanes, where down-trimming tail loads operate on longer moment armsto the airplane'scenter of gravity.

According to Duane McRuer, the designers of the YB-49 gave a great deal of thought to flying that airplane with unstable loadings, to take advantage of the performance gains. However, Waldemar O. Breuhaus claims that the first actual application of superaugmentation wasmade on a North American AT-6 trainer. A Sperry airline-type A-12 automatic pilot flew the AT-6 quite successfully with a negative static margin of 6.7 percent of the wing chord. In current practice, the General DynamicsF-16 wasdesigned to fly with a slight negative static margin. Depending on store loadings, this is the case in practice. To reduce horizontal tailtrim loadsduring cruise, fuel ispumped into cellsin the horizontal tailsof the McDonnell DouglasMD-11 and the Boeing 747-400.

There are two general pathsto superaugmentation. The most obviousisto artificially increase back to stable levels those derivatives that characterize longitudinally unstable airplanes. These are the derivatives *M*α, *Mq* , and *Mu*. Feedbacksto the longitudinal control of angle of attack, pitching velocity, and airspeed, respectively, are required. However, there are practical problems with feeding back angle of attack and airspeed signals at high gain. Vertical and horizontal air turbulence components appear as objectionable noise inputs. Atmospheric turbulence noise effects may be partially compensated with complementary filters, which replace the higher frequency atmospheric turbulence signals with their inertially derived equivalents, inertial vertical and horizontal velocity. The airframe thus acts as a filter on the high-frequency turbulence signals.

The alternate path to superaugmentation relies on inertially based signals, such as pitching velocity, derived pitch attitude, and normal acceleration. Inertial signals lend themselves to modern redundant mechanizations. For example, five or six rate gyros in a skewed orientation can provide fail-operational capability for all three airplane axes. Figure 20.5 illustrates

![5 illustrates](../assets/chapter20/_page_10_Figure_5.jpeg)

**Figure 20.5** Example of a block diagram for an inertially based superaugmentation system for longitudinally unstable airplanes. The denominator s in the Equalization box integrates the pitching velocity error signal *qe*, providing a pseudopitch attitude signal. (From Myers, McRuer, and Johnston, NASA CR 170419, 1984)

![Chapter 20 - Figure 1](../assets/chapter20/_page_11_Figure_1.jpeg)

**Figure 20.6** Block diagram for the X-29A research airplane superaugmented pitch control system, designed to overcome unstable static margins of up to 35 percent of the wing mean chord. Pitch angular acceleration is synthesized with filtered canard position. Normal acceleration feedback provides proper stick force per g. (From Clarke, Burken, Bosworth, and Bauer, NASA TM 4598, 1994)

superaugmentation by pitch rate feedback, integrated for a derived pitch attitude (McRuer, Johnston, and Myers, 1985). An aperiodic divergence caused by static longitudinal instability is eliminated as system gain is increased. A new longitudinal short-period mode appears with relatively high damping and frequency, making possible precision attitude control, provided that proper attention is paid to flight path response (Gibson, 1995). Large stability marginsare attained. Thisprovidesrobustnessagainst parameter changes. The X-29A pitch control system, illustrated in Figure 20.6, is another inertially based superaugmented case.

Control system rate or position saturation can be particularly deadly for superaugmented airplanes. Once the control surfaces are operating at actuator-limited rates or against the surface stops the design reverts back toward the unaugmented, or unstable, case. In design studies, one must identify the command or disturbance levels that could cause unacceptable divergences due to control rate and position saturation.

### **20.11 Propulsion-Controlled Aircraft**

Multiengine airplanesthat rely on hydraulically powered controlscan be controlled in an emergency by differential applicationsof thrust. Thisisfor the emergency situation in which all control surfaces are either fixed or freely floating, but are no longer under the control of the flight crew. NASA callsairplanescontrolled by differential operation of thrust propulsion-controlled aircraft, or PCA.

While differential thrust might in principle provide sufficient control moments to guide an airplane to a safe emergency landing, it should be clear that lags in engine thrust response to throttle movements would make successful control an almost impossible task. The emergency noted in Sec. 5.23, "Safety Issues in Fly-by-Wire Control Systems," where a Lockheed L-1011 with a jammed elevator wascontrolled with differential thrust by a highly skilled pilot, did not involve full loss of flight control operation. A rather less successful outcome of differential thrust control occurred with a DC-10 that had lost all flight control operation (Tucker, 1999).

The difficulty of throttle-only control for emergency control of airplaneswith failed control systems led NASA to authorize a research program for propulsion-controlled aircraft that would lead to workable systems. The key concept was the use of stability-augmentation techniques that would overcome the thrust lag problem, without requiring unusual pilot skills. The research was authorized by the then director of NASA's Dryden Flight Research Center, Kenneth J. Szalai, and took place starting in 1990 (Burken and Burcham, 1997).

The NASA PCA program wascarried far enough to prove in flight testing that in the absence of surface hardovers or large mistrim conditions, a three-engine commercial jet, the MD-11, could be returned to an airport and landed without the aid of aerodynamic surfaces. The tail engine was used in the tests, although the PCA system is designed primarily for airplaneswith two wing engines. The MD-11 engineswere modified for PCA operation with full-authority digital controls and special idle settings to avoid large time lags in response to thrust change commands. The longitudinal and lateral PCA control laws are illustrated in Figure 20.7. In conclusion, the NASA PCA effort has provided a viable option, with

![In conclusion, the NASA PCA effort has provided a viable option, with](../assets/chapter20/_page_12_Figure_3.jpeg)

**Figure 20.7** Longitudinal (*above*) and lateral (*below*) control laws used in the NASA Propulsion-Controlled Aircraft (PCA) demonstration using a MD-11 jet. (From Burken and Burcham, 1997).

moderate hardware and software costs, for transport designers to consider in the quest for safety.

#### **20.12 The Advent of Digital Stability Augmentation**

Airplane digital fly-by-wire flight control systems, which make possible digital stability augmentation, go back to the 1970s. Priority is difficult to establish, since many organizationswere doing thiswork at about the same time. One early application wasat the NASA Dryden Flight Research Center, using digital flight hardware from the Apollo program. Although overdesigned in many ways for the airplane application, it made possible an early demonstration of the possibilities of airplane digital augmentation.

That program used a Vought F-8C airplane (Jarvis, 1975). The first step was to fly single-channel digital flight control systems on the F-8C, with backup analog controls in case of failure. The next step was a big one from the standpoint of system complexity: the development of a triplex digital system, using redundancy management and data bus concepts. The subsequent routine use in modern airplanes of redundant, fail-operational digital flight control and stability augmentation is at least partially the result of this early NASA effort.

Another early application was the quadruplex redundant digital fly-by-wire system flown in the BAe FBW Jaguar. Design commenced in the late 1970s, and it flew between 1981 and 1984 in configurationsranging from normal to highly unstable. The BAe FBW Jaguar technology led to the EAP (Experimental Aircraft Programme) and ultimately to the Eurofighter.

#### **20.13 Practical Problems with Digital Systems**

When digital stability-augmentation systems first appeared, their most alluring advantage, as compared with analog systems, was their ability to change system gains, shaping networks and even architecture by software changes, instead of requiring timeconsuming hardware changes. This is especially attractive in a prototype flight testing program, asmay be imagined. However, a drawback to thiscapability isthat the ease of making changesby software modificationsencouragesa cut and try approach to fixing problems.

The same design freedom that makes for easy changes in a digital stability-augmentation system makes it easy to load the design with overly complex gain schedules and cross-feeds. In a recent classified program, practically all system gains are complex functions of altitude, Mach number, angle of attack, center of gravity, and other measurable parameters, with no real proof that this complexity is needed. One result of complex gain schedules is an inordinate amount of time required for checkout in simulation and flight testing.

On the hardware side, one can be faced with digital flight control systems that incorporate several sampling systems, operating at different rates and not in synchronization. This is the case on the Grumman X-29A digital flight control system. Again, careful simulation and bench testing is needed to be sure that no problems arise from this. Anti-aliasing filtersare generally needed on the inputsof analog-to-digital converters, to screen out input frequenciesthat are multiplesof the digital sampling frequency.

### **20.14 Time Domain and Linear Quadratic Optimization**

Control system synthesis in the time domain, rather than in the frequency domain, isoften called modern control theory. Optimal controller design isgenerally involved. Although one usually thinks of modern control theory in connection with full automatic control, it is applied as well to the design of stability-augmentation systems.

Linear quadratic (LQ) optimization methods have been used for a number of stabilityaugmentation system designs. These methods have their origins in the work of R. E. Kalman. Airframe and controller equations are cast in the state matrix form discussed in the previous chapter. The optimal controller isa linear feedback law that minimizesan integral cost function *J* of the form

$$J = \int [\mathbf{x}^\mathsf{T} \mathcal{Q} \mathbf{x} + \boldsymbol{\delta}^\mathsf{T} \boldsymbol{R} \boldsymbol{\delta}] dt,$$

where *x* is the system state vector, δ isthe control vector, and *Q* and *R* are weighting matricesthat expressthe designer'sideason what constitutesoptimal behavior for thiscase. The optimal control law takesthe form of a linear set of feedback gains δ = *Cx*, where *C* is the gain matrix of constants. The gain matrix *C* iscomputed by a matrix equation called the Riccati equation.

The linear quadratic approach to controller design is attractive because it is an organized method for finding feedback gains. The method produces an optimal set of feedbacks, but only for the arbitrarily chosen weighting matrix values. One can argue that if the weighting matrix values are poorly chosen, the resulting system can be far from ideal. In fact, it is not uncommon for designers using linear quadratic methods to tinker with weighting matrix values until a reasonable-looking system emerges. This puts the optimal design method on all fourswith ordinary cut-and-try methods.

The problem of assigning weighting matrix values aside, there have been numerous variantsof the linear quadratic approach to controller design and any number of applications in the literature and in practice. A typical application isto the design of a lateral-directional command augmentation system (Atzhorn and Stengel, 1984). The criterion function includes control system rate as a means of limiting high-frequency or rapid control motions. Displacement and rate saturation are significant nonlinearities that cannot be treated with the linear quadratic approach, except by the use of describing functions (Hanson and Stengel, 1984). Other linear quadratic stability-augmentation designs that may be found in the literature include departure-resistant controls, superaugmented (unstable airplane) pitch controls, and multiloop roll–yaw augmentation.

According to Robert Clarke and his associates at the NASA Dryden Flight Research Center, the Grumman X-29A research airplane'sflight controlswere originally designed using an optimal model-following technique. Simplified computer, actuator, and sensor models were used in the original analysis, leading to an unconservative design. A classical approach was chosen in the end, with lags introduced by the actual hardware compensated for by the addition of lead-lag filters(Clarke, Burken, Bosworth, and Bauer, 1994).

Another interesting linear quadratic stability augmentation design adds feed-forward compensation for nonlinear terms that cannot be included in the linearized design. This is the stability-augmentation system for the Rockwell/Deutsche Aerospace X-31 research airplane. Feed-forward compensation is added for nonlinear engine gyroscopic and inertial coupling effects(Beh and Hofinger, 1994).

### **20.15 Linear Quadratic Gaussian Controllers**

Linear quadratic Gaussian (LQG) controllers add to the linear quadratic (LQ) designs random disturbances and measurement errors. LQG designs are discussed at length in a 1986 text and a 1993 IEEE paper by Professor Robert F. Stengel. The form taken by

![Chapter 20 - Figure 1](../assets/chapter20/_page_15_Figure_1.jpeg)

**Figure 20.8** Various control system forms that can be represented with the structured linear quadratic regulator (LQG) method. (From Stengel,*IEEE Trans. on Systems, Man, and Cybernetics*,c 1993 IEEE)

the discrete-time LQG optimal controller is

$$
\mu\_k = C\_F \mathbf{y}\_k^\* - C\_B \mathbf{x}\_k,
$$

where *yk* <sup>∗</sup> isthe desired value of an output vector and *xk* is the Kalman filter state estimate.

The LQG design approach is very flexible because of the number of parameters that can be chosen arbitrarily. At one extreme, a scalar one-input, one-output design can be produced. Measurement and control redundancies can be represented if measurement and control vector sizes exceed that of the state vector. Also, integral compensation and explicit model-following structures can be produced (Figure 20.8).

LQG designs are among the most advanced to be in use by stability-augmentation engineers, asthisiswritten. Even more advanced control conceptscontinue to pour out of university and other research centers. The same 1993 paper by Stengel cited above provides a good survey of advanced control concepts, including expert systems, neural networks, and intentionally nonlinear controls.

#### **20.16 Failed Applications of Optimal Control**

The failure of optimal control methods to produce a satisfactory flight control system for the Grumman X-29A airplane was noted in Sec. 14. This failure is by no means an isolated event. Additional instances can be found in which optimal control methods in the hands of experienced engineers have failed to produce safe and satisfactory flight control systems. What has gone wrong? Several experts who have witnessed these failures discuss the problem:

- **Phillip R. Chandler and David W. Potts (1983), U.S. Air Force Flight Dynamics Laboratory** "[T]he infinite bandwidth constant compensation elementswhich are required [for LQR] violate the very heart of the feedback problem. . . . LQR therefore isan elegant mathematical solution to a nonengineering problem. . . . SVT (Singular Value Theory) [Doyle, 1979] isa very crude method of coping with uncertainty in the LQR or LQG procedure. It makes assumptions that are not valid for flight control. . . . LQR with all its ramificationsand refinementsistotally unsuited for the flight control servomechanism problem."
- **John C. Gibson (2000), formerly with English/Electric/British Aerospace** "[Robert J.] Woodcock told me that there have been several missile and aircraft projects in serious trouble due to the use of such [LQG] methods. . . . While optimization methodsare continually being improved, they cannot yet (and may never) guarantee a safe and satisfactory FCS [flight control system] design without the strictest guidance and detailed physical understanding of experienced control and handling qualitiesengineers. Thisistrue for highly advanced and demanding types of aircraft. Every signal path must be clearly visible and easily related to specific aerodynamic or inertial characteristics of the airframe. In simple aircraft without complexity, there is no advantage over straightforward engineering methodsanyway."
- **Michael V. Cook (1999, 2000), Senior Lecturer, Cranfield University** "There exists an enormous wealth of published material describing the application of so-called, 'modern control methods' to the design of flight control systems for piloted aeroplanes. It is also evident, with the exception of a very small number of recent applications, that there is a conspicuous lack of enthusiasm on the part of the airframe manufacturers to adopt this design technology, especially for the design of command and stability augmentation systems for piloted airplanes. Having an industrial background I am well aware of the many reasons why modern control has not been taken onboard seriously by the manufacturers – academic control specialists don't share my view, and in many cases probably don't even understand it! . . . I know that my views are shared by the control people in —— who, in private are not at all complimentary about the academic control specialists in the UK. I am also aware that the Boeing view is similar to that of —— . I've seen some appallingly bad control systems design theses (not from Cranfield)."
- **Steven Osder (2000), Osder Associates, Arizona** "We [Osder and Dunstan Graham] used to lament the absurdity of papers [on robustness theory] that were filling the journals and we amused each other by citing specific examples of such departures from reason and logic. . . . At the [Boeing] helicopter company, we took each of those University of – [robust flight control] designs and tested them against more complete [nonlinear] models of the [Apache] aircraft.

In every case, these robust flight control designs always fell out of the sky. In one case [which used eigenstructure assignment], even testing against a linear model, but with only a 10 percent variation in a single B [control] matrix term, our simulations resulted in a crash."

**Duane T. McRuer (2001), Chairman, Systems Technology, Inc.** "At STI we have spent an enormous amount of time and effort searching for ways to make optimal control practical – at least 20 major reports and papers, with some tremendously capable folk (e.g., Dick Whitbeck, Greg Hofmann, Bob Stapleford, Peter Thompson, et al.). Our focushasbeen on finding performance indices, special schemes, etc., to make optimal control solutions jibe with good design practice. . . . We have just never been happy with the results for stability augmentation design."

In the light of the foregoing comments, a design case (Ward, 1996) in which an LQG design for a pitch stability augmentation system was used only as a guideline for a more conventional approach suggests a reasonable use for optimal control techniques. The concept of using LQR optimal control synthesis as a guide or in conjunction with classical methods is also developed by Blight (1996). Blight also comments that LQR methods should be used only on "control problemsthat actually require modern multivariable methodsfor their solution." For example, Blight recommends ordinary gain scheduling instead of attempting to design a single robust linear control law for all flight conditions.

#### **20.17 Robust Controllers, Adaptive Systems**

Robust flight control systems are designed specifically to perform well in the face of airframe, sensor, and actuator uncertainties and even failures. An early robust flight control system approach was the adaptive control system, a particular research objective of the Honeywell Corporation. Thiswasin the daysbefore airborne digital computers. The modest objective wasto identify the airplane'spitch natural frequency by periodic injection of small test pulses of elevator control. Pitch natural frequency variations reflected changes in both center of gravity location and dynamic pressure, or calibrated airspeed. Control system gain was lowered at the higher pitch natural frequencies to maintain system stability.

Modern applicationsof adaptive control make use of parameter identification, although test signals are still required to keep the parameter identification loop from going unstable. In a 1982 NASA workshop on restructurable controls, reasonably good results were reported for two adaptive schemes (Cunningham, in Montoya, 1983). Horizontal tail effectiveness *M*<sup>δ</sup> wasidentified on a Vought F-8 sufficiently well for autopilot gain scheduling through the flight envelope. Also, the flutter modes of a wind-tunnel model of a wing with stores (weapons) were identified by maximum likelihood methods.

The same NASA workshop brought a theoretical criticism of all adaptive systems by MIT professor Michael Athans. In his words:

Over two thousand papers have been written [on adaptive control] and a lot of excitement generated. You may have seen that people are giving courses to industry on how to make adaptive control practical. We have a recent MIT Ph.D. thesis [Rohrs, 1982] finished in November 1982 that Dr. Valvani and I supervised, which proved with a combination of analytical techniques and simulation results that all existing adaptive control algorithms are not worthwhile.

The algorithms may look excellent if you follow their theoretical assumptions, but in the presence of some persistent output disturbances and unmodeled high frequency dynamics all adaptive control algorithms considered become unstable with probability one.

Aside from coping with center-of-gravity and flight condition changes, robustness in control systems already exists in augmentation systems incorporating self-checking redundant digital computers. Robustness against sensor failures has also been demonstrated with redundant inertial sensors in skewed orientations. Failure of one or two sensors leaves the system fully operational. Failure of a single airspeed meter due to icing resulted in the losses of a General Dynamics B-58 Hustler and of an US/German X-31A research airplane. The automatic pilot gain-changing featuresinterpreted the iced meter readingsaslow airspeed, requiring higher gains(communication from Dr. Peter Hamel).

Robustness against actuator failures, and especially against failures that result in control surfaces that go hard over against a stop and stay there, is another matter. The stirring example of Delta Airlines' pilot McMahan who saved a Lockheed 1011 with one elevator against the up stop is told in Chapter 5, "Managing Control Forces." System concepts for reconfiguring control systems to cope automatically with major failures are still in the early stages.

While waiting for the development of systems that are robust in the face of actuator hardovers, Thomas Cunningham suggests two straightforward aids for the human pilot. The position of each individual control surface should be measured and displayed in the cockpit. Captain McMahan did not know that the 1011 elevator was against its stop. Also, engine controllers should be designed to the higher bandwidths needed for differential thrust control of a crippled airplane.

#### **20.18 Robust Controllers, Singular Value Analysis**

The analysis of robust controllers took a different tack from adaptive controls with the work of J. C. Doyle and his associates, starting around 1980. The key to the new approach is a generalization of system gain using the singular values of a matrix. Matrix singular values are another term for the matrix norm, defined as the square root of the sum of the squares of the absolute values of the elements. The matrix norm is the trace of *A*∗*A*, where *A* isthe given matrix and *A*<sup>∗</sup> isthe Hermitian conjugate of *A* (or the transpose if *A* is real).

According to the singular value approach, control system robustness against uncertainties in mechanical and aerodynamic properties is assured if the amplitude of the maximum expected uncertainty is less than the minimum system gain at all frequencies.

A simpler, but equally important application of singular value analysis is to system stability margins, without considering uncertainties. Stability margins are guaranteed if the minimum singular values of the system's return difference matrix are all positive (Mukhopadhyay and Newsom, 1984). The system return difference matrix *I* + *G* isa matrix generalization of the closed-loop transfer function denominator for a single-input single-output system. This stability margin application of singular value analysis was made for the X-29A research airplane (Clarke et al., 1994).

# **20.19 Decoupled Controls**

Airplane stability augmentation must be rethought when designers choose to add direct normal and side force control surfaces. For example, with direct lift control through a fast-acting wing flap, pitch attitude can be controlled independently of the airplane's flight path, and vice versa. The utility of such decoupled controls for tracking, defensive maneuvers, and for landing approaches is reviewed by David J. Moorhouse (1993).

#### **20.20 Integrated Thrust Modulation and Vectoring**

An airplane's propulsion system can be integrated into a stability augmentation system that uses aerodynamic control surfaces. The total system would operate while the airplane remainsunder the control of the human pilot, qualifying asa stability-augmentation system rather than as an automatic flight control system.

For comparison, the previous coverage of propulsion systems in this book included:

- **Chapter 4** the effectsof conventional, or fixed-configuration, propeller-, jet-, and rocket-propulsion systems on stability and control;
- **Chapter 10, Sec. 8** thrust vector control to augment aerodynamic surfaces in supermaneuvering;
- **Chapter 11, Secs. 14 and 15** propulsion effectson modesof motion and at hypersonic speeds;
- **Chapter 12, Sec. 1** carrier approach power compensation systems, for constant angle of attack approaches;
- **Chapter 20, Sec. 11** Propulsion-controlled aircraft, designed to be able to return for landing after complete failure of normal (aerodynamically implemented) control systems.

Depending on the number of enginesunder control, thrust modulation and vectoring systems can supply yawing, pitching, and rolling moments, as well as modulated direct forces along all three axes. Thus, thrust modulation and vectoring integrated into a stabilityaugmentation system can augment or replace the aerodynamic yawing, pitching, and rolling moments provided by aerodynamic surfaces. The situation is similar to aircraft like the Space Shuttle Orbiter, which carries both aerodynamic and thruster controls. However, in the context of stability augmentation, thrust modulation and vectoring would be used normally at the low airspeeds of approach and landing, rather than in space.

While in principle thrust modulation and vectoring can take the place of aerodynamic control surfaces at the low airspeed where the aerodynamic surfaces are least effective, it is reasonable to ask whether thrust stability-augmentation systems could satisfy flying qualities requirements. In a simulation program at DERA, Bedford (Steer, 2000), integrated thrust vector control was evaluated at low airspeeds on the baseline European Supersonic Commercial Transport (ESCT) design. The nozzles of all four wing-mounted jet engines were given both independent pitch and yaw deflections, providing yawing, pitching and rolling moments. Nozzle deflections were modeled as first-order lags. Conventional pitch rate, pitch attitude, velocity vector roll rate and sideslip command control structures were programmed.

Pitch control by thrust vectoring at approach airspeedswasasgood asaerodynamic or elevon control, for a reason peculiar to the very low wing-aspect-ratio ESCT configuration. That is, the airplane hashigh induced drag at approach anglesof attack, requiring large levelsof thrust to maintain the glide path, thusmaking available large pitching moments with thrust deflection. Low airspeed roll and sideslip thrust vector control were positive and suitably damped but did not satisfy MIL-STD-1797A criteria.

### **20.21 Concluding Remarks**

Airplane stability augmentation was born with the B-47 and B-49 systems around 1947. Available analysis methods were at hand in the frequency-based Nyquist and Bode methodsdeveloped by electrical engineers. More advanced time-domain analytical concepts appeared about the time an airborne digital flight control computer flew in an F-8C at the NASA Dryden Flight Research Center.

Today's stability and control designer has a remarkably wide choice of modern flight control theoretical conceptsto select from and mature digital control hardware to correspond. The expansion of new modern flight control theory shows no signs of tapering off. As always, a moderating factor in selecting any advanced concept is the cost of a thorough validation on an actual project. A recurring theme among design engineersisfailure of modern control theory to produce practical flight control system designs. M. V. Cook notes that modern control methodsmay have more relevance to pilotlessaircraft because their performance is more easily defined in purely mathematical terms.

The likelihood is that advanced flight control system concepts will not be adopted in inexpensive personal aircraft, regardless of cost, simply because possible gains in performance and safety will not be there. The same is likely in light commuter transports. However, performance gains with relaxed static stability or superaugmentation become significant for long-range subsonic transport airplanes. Robustness in their flight control systems should help bring about thisapplication and the opportunity for controlsdesigned by optimal, singular-value, neural network, or advanced methods not yet imagined. The case for relaxed or even negative static stability is even stronger for supersonic cruise transports. Two limiting factorsare the required pitch control momentsto recover from upsetsand the interaction with flexibility modesof the high-bandwidth actuatorsneeded to cope with unstable airplanes.

Finally, military airplanes should be where advanced techniques, such as departure resistance, decoupling, real-time vehicle system identification, active flexible wings, integrated thrust vectoring and modulation, and self-repairing controls, will get serious consideration and possible application.