# *Naval Aircraft Problems*

Airplanesoperating from aircraft carriershave stability and control problemsnot present in land-based airplanes. Some problems arise from the size constraint, to allow airplanesto fit on the elevatorsof asmany carriersaspossible. For stability and control engineers this translates into restrictions on tail length, since wings can be folded. Good pilot visibility over the nose is needed for nose-high landing approaches, affecting the airplane's design at many points. Waveoffs or missed approaches must be made starting from more adverse airspeed and attitude conditions than from field landings. This means positive, safe control near the stall and careful integration with the airplane's performance design.

Finally, there is the matter of carrier landings. From the moment of starting a final approach to either field or carrier landings an airplane's path and airspeed must be controlled. Path control isneeded to make a touchdown in the correct area, with a reasonable vertical velocity. Airspeed control is needed to keep the touchdown speed within limits. Depending on the on-board avionic equipment, weather conditions, and pilot training and preferences, path and airspeed control for field landings use a variety of visual cues and instrument readings. The important point is that touching down at a precise point is seldom required for field or airport runway landings.

In contrast to the airport runway case, touchdown point precision to within a very few feet is necessary for successful landings on aircraft carriers. Carrier landings are made without flare. Thus, low approach speeds are desirable to reduce touchdown vertical velocity and landing gear loads. There is little tolerance for errors in touchdown airspeed between stalling and excessive speed, leading to hard landings. As a result, carrier landing accidents, mainly due to hard landings and undershoots, are statistically more common than airport landing accidents.

# **12.1 Standard Carrier Approaches**

Naval aviatorshave developed a distinctive landing approach procedure to make touchdown point precision a routine matter. U.S. carrier-based airplanes turn onto a short final approach path in a steep left turn, avoiding as much as possible the ship's turbulent wake or burble. Carrier final approachesare typically lessthan 3/4 mile long, taking some 15 to 20 seconds to complete (Craig, Ringland, and Ashkenas, 1971).

In manually flown approachesthe pilot relieson an optical projection device for a vertical reference, rather than the view of the ship's landing area. The optical device, mounted on the carrier's deck, is gimbaled to project a stable glide slope. The pilot sees a projection of a solid circle and short horizontal datum bar. Below the glide slope the ball appears below the bar, and vice versa. Radar-controlled automatic carrier landings have also been developed, using an SPN-42 tracking radar mounted on the ship. Aircraft attitude changes are sent ascommandsto the airplane'spitch attitude autopilot, to correct perceived height errors relative to the ideal glide path.

![Chapter 12 - Figure 1](../assets/chapter12/_page_1_Figure_1.jpeg)

**Figure 12.1** Block diagram for the AN/ASN-54 Approach Power Compensation System. This was designed for carrier airplanes to hold the angle of attack constant using thrust variations. However, path control was unsatisfactory using this system. (From Craig, Ringland, and Ashkenas, Syst. Tech., Inc. Rept. 197-1, 1971)

In order to control airspeed closely, the final approach is made at a constant angle of attack. Precise control of angle of attack asa meansof controlling airspeed isconsidered so important that a special throttle control system – the Approach Power Compensation System, or APCS – was developed for that purpose. There were many experiments with different feedbacks; the final APCS design uses angle of attack and normal acceleration feedbacks to the throttle and some pilot stick feedforward (Figure 12.1).

# **12.2 Aerodynamic and Thrust Considerations**

It hasbeen known for some time that landing approach path control by elevator or pitch adjustments does not work for low-aspect-ratio (stubby) straight or sweptback wings. Thisisdue to the variation of drag with airspeed when the lift isequal to the grossweight in level flight conditions. We normally expect level-flight drag to increase rapidly with increasing airspeed, and so it does at cruising airspeeds. At cruising airspeeds height control by pitch attitude changesusing the elevator isstable and effective. The throttle can be left fixed.

However, the level-flight drag for any airplane increases with decreasing airspeed near the stall, as a result of induced drag increases and flow separation at high angles of attack. Asairspeed isreduced from cruising valueslevel-flight drag reachesa minimum and then actually increases again as the airspeed is reduced still further. The airspeed at which levelflight drag, and thrust required to hold level flight, reach minimums was given the name "minimum drag speed" by Stefan Neumark in Britain (1953).

The increase in level-flight drag near the stall is accentuated for airplanes with low-aspectratio wings, leading to increases in minimum drag speed. The minimum drag speed for an airplane with a low-aspect-ratio wing can be well above the low approach airspeed desired for carrier landings. Thus, if an airplane with a low-aspect-ratio wing is on a stabilized descent at a low landing approach speed typically used for aircraft carriers and the pilot retrims the airplane to a higher angle of attack, reducing airspeed, the airplane will rise at first relative to the original path and then settle even faster. The flight path will become steeper, a counterintuitive result.

For landing approaches below the minimum drag speed, where increasing thrust is required for decreasing airspeed in level flight, sometimes called "the back side of the thrust required curve," pitch attitude control by the elevator is unsatisfactory, even with the throttle used to control height. Thrust control by the pilot or an automatic system (the Navy's APCS) to hold constant airspeed or angle of attack has been used to artificially create the normal variation of thrust required for level flight.

"Backside" carrier-based approach problems were first recognized about 1950 (Shields and Phelan, 1953). Pilots needed to use higher approach speeds for the XF-88A and XF3H-1 airplanes than the standard rules of thumb based on stalling speed. Shields and Phelan proposed a fixed-throttle pitch-up test maneuver that is similar to a popup maneuver later adopted as one criterion for minimum carrier-approach speed. The first large-scale organized set of data on minimum approach airspeed behavior for jet airplanes was taken at the NACA AmesAeronautical Laboratory (White, Schlaff, and Drinkwater, 1957). Carriertype landing approaches were made with seven straight- and swept-wing jet airplanes, the FJ3, F7U-3, F9F-6, F4D, F-100A, F-94C, and the F-84F. The objectivesof the 1957 Ames tests was to find the minimum "comfortable" approach airspeeds for carrier-type landings for these representative jet airplanes.

The reason most frequently given by the NACA Ames pilots for minimum approach airspeeds was inability to control precisely altitude or flight path at lower speeds. However, there was a surprising lack of correlation between the minimum comfortable approach airspeed and the Neumark minimum drag speed. For example, Ames pilots set the minimum comfortable approach airspeed for the Douglas F4D-1 Skyray at 121 knots, while the minimum drag speed is 152 knots. Similar results appeared with the North American F-100A Super Sabre, where a minimum approach airspeed of 145 knotswasselected, ascompared with the minimum drag speed of 150 knots (Figure 12.2). Clearly, some other factors than inability of the elevator or stabilizer to control height without reversal were critical.

Another set of carrier-approach tests (Bezanson, 1961) found that flight path control of the Vought F8U and DouglasF4D-1 airplanesat low landing approach speedsrequired use of the throttle and was not satisfactory by angle of attack or pitch control modulation alone. Bezanson found that with thrust modulation as the primary path controller the dynamic characteristics of the thrust control system became important, including such factors as throttle friction and breakout force, throttle sensitivity (pounds of thrust per inch of throttle movement), and thrust time lag following abrupt throttle movements.

In contrast to pure jet engines, turboprops are operated at high RPMs all the time. Thrust modulation is done by propeller pitch changes, with very small time lags. The poor engine dynamic behavior of pure jet engines, particularly engine thrust time lag at low power levels(Figure 12.3), kept U.S. Navy interest alive in turboprop combat airplaneslong after the U.S. Air Force had switched to pure jets. For example, the Douglas/Navy turboprop A2D-1 Skyshark made its first flight in 1950, the same year as the start of production on the Boeing/Air Force B-47A six-jet bomber.

# **12.3 Theoretical Studies**

The carrier-approach problem for naval aircraft received a great deal of attention from leading aeronautical research organizations, starting in the late 1950s. We note

![Chapter 12 - Figure 1](../assets/chapter12/_page_3_Figure_1.jpeg)

**Figure 12.2** Carrier landing approach airspeeds chosen by pilots are below the airspeed for minimum drag for both the North American F-100A (*top*) and the DouglasF4D-1 (*bottom*). (From White, Schlaff, and Drinkwater, NACA RM A57L11, 1957)

particularly contributionsto the theory by groupsat the NACA AmesAeronautical Laboratory, the Royal Aeronautical Establishment, and Systems Technology, Inc. Two main lines of investigation were prediction of the minimum acceptable carrier-approach airspeed for any airplane and the physics of optimum vertical path control during approaches.

![Chapter 12 - Figure 1](../assets/chapter12/_page_4_Figure_1.jpeg)

**Figure 12.3** Ling-Temco-Vought A-7E engine response characteristics. Lag in developing engine thrust is large at low power settings, creating path control problems in carrier approach. (From Craig, Ringland, and Ashkenas, Syst. Tech., Inc. Rept. 197-1, 1971)

The NACA Amesgroup examined some five candidate predictorsfor minimum approach airspeeds (Drinkwater and Cooper, 1958). As found earlier, minimum drag speed correlated poorly with minimum acceptable carrier-approach airspeed. Other performancerelated criteria were no better. Two that failed to correlate were the minimum airspeeds at which a given rate of change of flight path angle or a 50-foot climb could be obtained.

In the end, the Ames researchers concluded that a simple criterion based on stalling speed correlated best with the data. The minimum comfortable carrier-approach airspeed agreed best with 115 percent of the stalling speed in the power approach (PA) configuration, that is, flaps and landing gear down, power for level flight.

The Amesresult isvalid for airplanesof the general type tested, but one might be concerned at applying the 115-percent stalling speed prediction result to airplanes that differ radically from those tested. It seemed logical to try to develop a carrier-approach flight path model based on the fundamental flight and control dynamicsand human factorsof the problem. That was the motivation behind the work at Systems Technology, Inc., sponsored by the U.S. Navy. The STI engineers, including Tulvio S. Durand, Irving L. Ashkenas, Robert F. Ringland, C. H. Cromwell, Samuel J. Craig, Richard J. Wasiko, and Gary L. Teper, brought to the carrier-approach problem their well-known systems analysis techniques.

An interesting result, due to Ashkenas and Durand, identifies the transfer function parameter associated with minimum drag speed, the point at which height control by elevator becomes reversed from the normal sense. This is a numerator factor in the elevator to height transfer function called 1/*Th*1. Negative valuesof thisfactor put a zero in the right half of the *s*-plane. Closing the height to elevator loop results in an aperiodic divergence corresponding to the reversal of normal height control below the minimum drag speed.

Around 1962, Ashkenas came up with the first systems analysis basis for minimum carrier-approach airspeed prediction. That is, his prediction for minimum approach airspeed was based on assumed pilot loop closures with an airframe defined by arbitrary mass, aerodynamic, and thrust characteristics (Ashkenas and Durand, 1963). Since the systems analysis approach does not merely correlate the behavior of existing airplanes, the results should apply to airplanes not yet built whose characteristics are beyond the range of those tested so far.

The Ashkenas-Durand systems analysis prediction for minimum carrier approach airspeedscan be explained asfollows:

- 1. The approach is assumed to be made in gusty air.
- 2. In gusty air the pilot attempts to close the pitch attitude loop at a higher frequency than the gust bandwidth, or as high a frequency as possible.
- 3. The highest possible pitch attitude loop bandwidth occurs when the pilot's gain is so high that the closed-loop system is just neutrally stable.
- 4. By excluding pilot model leadsand lags, or treating the pilot asa pure gain, a definite gain value is associated with the neutrally stable closed pitch loop.
- 5. Similarly, an outer altitude control loop is closed by the pilot using pure gain, or thrust proportional to altitude error.
- 6. With both pitch and altitude control loops closed by the pilot, the sensitivity of the pitch control loop break frequency to pilot pitch control gain iscalculated, as a partial derivative.
- 7. The sign of this partial derivative of pitch loop bandwidth to pilot pitch control gain, called the *reversal parameter*, istaken asan indication of carrier-approach performance. Positive reversal parameter values mean that increasing pilot gain improvesbandwidth and performance.
- 8. The lowest airspeed at which the reversal parameter is positive is taken as a prediction of minimum carrier-approach airspeed.

The reversal parameter was refined in subsequent studies by Ashkenas and Durand in 1963 and by Wasicko in 1966. An interesting consideration was the finding in 1964 by Durand and Teper that the carrier-approach piloting technique asthe airplane nearsthe carrier ramp changes from that assumed in the reversal parameter model. However, the approach airspeed would have already been set in the early part of the approach.

A later (1967) study of the carrier-approach problem by Durand and Wasicko went into the problem in greater detail, including the dynamicsof the optical projection device that pilotsuse asa glide slope beam. The 1/*T*θ<sup>2</sup> zero in the pitch attitude to elevator transfer function turned up as a primary factor, both in simulation and in landing accident rates. Unfortunately, thiszero isdominated by airplane lift curve slope and airplane wing loading. Lift curve slope in turn is fixed by wing aspect ratio and sweep.

Wing loading, aspect ratio, and sweep are among the most fundamental of all design parametersfor an airplane, affecting itsflight performance. When a new carrier-based airplane is being laid out and wing loading, aspect ratio, and sweep are being selected to maximize such vital factors as range and flight speed, it is hard to imagine that a statistical connection with landing accident rate will be prominent in the trade-off.

Systems analysis methods were applied again to the carrier-approach problem in 1990 by Robert K. Heffley of Los Altos, California. Heffley studied the factors that control the carrier-approach outer loop involving flight path angle and airspeed. The higher-frequency pitch attitude inner loop was suppressed in the analysis, assumed to be tightly regulated by the pilot.

Heffley closed the outer loop under three different strategies, depending on whether the airplane was on the front side or back side of the drag required curve. The results give interesting insights into factors affecting the approach (Heffley, 1990). Another study in this series is an application of the Hess Structural Pilot Model (discussed in Chapter 21) to the carrier-approach problem, using a highly simplified pilot–airframe dynamic model.

The current U.S. Navy criterion for minimum carrier-approach speed, as exemplified by the system specification for the F/A-18 Hornet, gives no fewer than six possible limiting airspeeds, such as the lowest speed at which a 5-foot per second squared longitudinal acceleration can be attained 2.5 seconds after throttle movement and speed brake retraction. Heffley concludesthat two additional criteria might be needed. One isa refinement of existing lag metrics to one that combines coordinated pitch attitude and thrust inputs. The other isan extension of the popup maneuver dealing with the end game, when the airplane isquite near the carrier'sramp.

# **12.4 Direct Lift Control**

Direct lift control, in which airplane lift ismodulated to correct flight path errors without changing airplane angle of attack, seems to be a natural solution to carrier-approach path control problems. According to William Koven, the first proposal for direct lift control on carrier airplanescame from DouglasE. Drake, a DouglasAircraft engineer and former Navy pilot. Professor Edward Seckel directed follow-up studies at Princeton University. Direct lift control was first tested on a carrier-based airplane in 1964. This was a Ling-Temco-Vought F-8C, modified for the aileronsto act asvariable flaps. That work wasdone by J. D. Etheridge and C. E. Mattlage.

The production Lockheed S-3A Viking hasdirect lift control, to aid in carrier landing approaches. On the S-3A, quite rapid flight path corrections are made by moving both wing spoilers, changing wing lift without changing the angle of attack (Figure 12.4). With direct lift control there isno need to wait for the airplane to respond in pitch to elevator motion, a response that takes place at the short-period pitching frequency of the airplane. A button on the S-3A pilot'syoke commandssymmetric spoiler deflection.

In contrast to the relatively crude button-operated S-3A direct lift control system, a sophisticated, integrated, direct lift system is used on the Lockheed 1011 Tristar, which is fitted with the CollinsFCS-240 digital automatic pilot. ThisCollinssystem, incorporating

![Chapter 12 - Figure 1](../assets/chapter12/_page_7_Figure_1.jpeg)

**Figure 12.4** Direct lift control using wing spoilers provide satisfactory path control for carrier landingson the Lockheed S-3A Viking. (From Jane's *All the World's Aircraft*)

automatic landingsor autoland, wasoriginally developed for the L-1011'sEuropean market, where the winter months require frequent low-visibility landings. The FAA certified the L-1011 for Category IIIA (ceiling zero, visibility 700 feet) landings in 1981.

When the pilot selects landing flaps the four inboard wing spoiler segments are rigged up to an 8-degree position. They are then modulated upward and downward from the up-rigged position to obtain direct lift control. Spoiler angle changes from the up-rigged position are commanded by the cockpit control column moved either by the pilot or the autopilot's autoland mode, in the normal sense. That is, back control column motion closes the spoilers and the airplane gainsaltitude.

If a control column adjustment is sustained for several seconds, the spoiler segment deflections from their up-rigged positions are gradually washed out and a corresponding adjustment is made to the horizontal tail angle. In the case of a sustained rearward control column motion, the washout moves the spoilers back up to their up-rigged positions of 8 degrees and the horizontal tail angle is increased in the airplane nose-up sense. The Tristar's period in the short-period pitching mode is a full 8 seconds at landing approach airspeeds. Pitch and path corrections by horizontal tail control alone would take place at that modal period, or rather slowly. Direct lift control provides a faster path response for demanding all-weather manual or automatic landings. In contrast to the S-3A case where the pilot controlsvertical path with the direct lift button aswell ascontrol column motion, in the integrated L-1011 case there is only one pilot controller, the control column.

What is missing in considering direct lift control for any airplane, carrier- or land-based, isa method that determineswhen that feature isneeded. What combinationsof pitch and thrust responses are such that direct lift control is required to meet specific vertical path control requirements?

#### **12.5 The T-45A Goshawk**

Thrust system dynamicsreappeared asmajor problemsmany yearsafter the Patuxent tests of the F8U and F4D-1 and the NACA, British RAE, and Systems Technology studies. Two carrier-based airplanes, the McDonnell Douglas/British Aerospace T-45A Goshawk and the Lockheed S-3A Viking, had similar problems (Wilson, 1992).

As a land-based trainer, the British Aerospace Hawk has a large speed brake or airbrake under the rear of the fuselage, aft of the wings, in the so-called ventral position. Extended, the speed brake would hit the ground when landing. The Hawk's speed brake is thus designed to retract into the fuselage automatically when the landing gear is lowered. In common with many subsonic jet airplanes, the Hawk's jet engine is the bypass variety. Bypass jet engines provide good low-airspeed performance, with high thrust levels, and they are fuel-efficient. However, high thrust at low airspeeds means that landing approaches are normally made at idle thrust settings, or low-engine RPM. Thus, if a go-around is required, a bit more time is needed to increase RPM to maximum than for an engine without bypass.

According to George Wilson's account, U.S. Navy test pilot Captain George J. Webb, Jr., asa carrier suitability expert, flew the original Hawk airplane in November 1983 to evaluate its behavior in simulated carrier approaches. Quoting from a draft of a memorandum from Webb to Rear Admiral E. J. Hogan, Jr., commander of the Naval Air Test Center:

Glide slope tracking [with speed brake not extended] was difficult, and corrections from high, low, and off speed conditions often resulted in numerous glide slope overshoots. Use of the ventral speed brake improved glide slope tracking and made any necessary corrections easier to accomplish.

Aircraft attitude changes associated with speed corrections were very small and difficult to discern. The combined effect made it difficult for the pilot to recognize an underpowered, decelerating situation sufficiently early to make timely corrections. Consequently, student pilots will occasionally land hard or short of the runway during syllabus flights not monitored by an LSO [Landing Signal Officer].

It was thought that the T-45A would be a straightforward conversion to naval use of a simple, existing training airplane. Thus, full-scale engineering development leading to production of 300 airplaneswaslaunched in 1984, concurrently with U.S. Navy flight tests of the Hawk, rather than after these had been completed. Some four years later, a first interim report on the McDonnell Douglas version, the T-45A, reported that the British Hawk landing approach deficienciesspotted by Captain Webb and othershad been built right into the new U.S. Navy airplane.

In the end, the Hawk's single-speed brake under the fuselage, where it cannot be used in landings, was replaced on the T-45A by a pair of fuselage side brakes. These are just ahead of and under the horizontal tail (Figure 12.5). Carrier landingsare made with speed brakes extended and at a high thrust level to overcome speed brake drag. At the higher thrust levels, modulation is rapid and effective in controlling the flight path. Also, just to be sure that student pilots stay out of path control trouble, the T-45A's flight idle RPM was increased from 55 to 78 percent of maximum, by adding an approach idle stop to the throttle mechanism.

There were other changesmade to the T-45A, relative to the Hawk, based on Navy flight tests. This all took place after full-scale engineering development had been started back in 1984. Hydraulically operated wing slats were added to increase wing maximum lift coefficient, a higher-thrust Rolls Royce Adour engine was installed to increase forward acceleration and reduce altitude losswhen a waveoff wasrequired, the vertical tail span

![Chapter 12 - Figure 1](../assets/chapter12/_page_9_Figure_1.jpeg)

**Figure 12.5** Path control problemsfor carrier landingsrequired changesto the McDonnell-Douglas T-45A Goshawk. Speed brakes were moved from the bottom to the side of the fuselage. (From Jane's *All the World's Aircraft*)

wasincreased, and a yaw damper and rudder-to-aileron interconnect wasadded to improve lateral-directional (Dutch roll) behavior. Captain Webb had complained about thisfollowing hisHawk flightsin 1983.

Also, bearing specifically on the thrust lag problem during carrier-landing operations, the Navy installed modified Lucasfuel controlson the T-45A'sAdour engines, to minimize thrust lag when power increases are called for. Finally, the speed brakes are interconnected to the horizontal stabilizer to minimize trim changes when the brakes are extended or retracted.

# **12.6 The Lockheed S-3A Viking**

Lockheed S-3A development followed a similar path to that for the McDonnell DouglasT-45A. That is, correctionsfor deficienciesfound in the 1973 flight testsof the fourth S-3A airplane were stretched out over the next ten years. The original S-3A design had the same problem in carrier approaches as did the original T-45A Goshawk. With jet bypass engines delivering enough thrust at low engine rotation speeds to stay on the final approach path, "If all of a sudden you're starting a settle coming into the carrier, you add power to regain altitude but nothing happensbecause of the delay in getting the enginesto respond" (Wilson, 1992).

In the case of the S-3A, the belated fix was the direct lift control system described previously. Another belated stability and control fix to the S-3A for carrier suitability is thrust trim compensation. The S-3A's low-slung engines produce longitudinal trim changes when power is used to adjust the final approach path angle, upsetting the desired constant angle of attack condition. The compensation movesthe elevatorsautomatically when the pilot adjusts the throttle position.

# **12.7 Concluding Remarks**

While the special carrier-approach problems for swept-wing jet airplanes have been recognized for over 30 years, there seems to be no clear-cut method for predicting the severity of such problems in preliminary design, much less for adopting solutions at an early stage. The detail specification for one of the U.S. Navy's recent jet airplanes, the McDonnell Douglas F/A-18, makes that point, listing no fewer than six possible determinants for that airplane'sapproach speed.

The closed-loop systems analysis approach to the carrier-landing problem would seem to offer the best chance of answering difficult questions, such as whether a new design will need direct lift control and what the upper limit might be for thrust lag following throttle motions. However, the closed-loop systems analysis approach apparently requires additional development before it is ready to be used in this design sense. Systems analysis study reports typically close with a "Need for Further Research" section.