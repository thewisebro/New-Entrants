<?php
	
	$alphabet = array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');
	
	$roman = array('i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv');

	$sections_B=array(
		'BUILDINGS',
		'TRANSPORTATION',
		'WATER',
		'ENERGY',
		'SOLID WASTE',
		'CLIMATE',
		'OTHERS'
	);
	$sections_D=array(
		'OPEN SPACE',
		'MAIN ADMINISTRATION BUILDING',
		'DEPARTMENTS',
		'HOSTELS',
		'STAFF ACCOMADATION',
		'HOSPITAL',
		'OTHERS'
	);
	$sections_E=array(
		'BUILDINGS',
		'TRANSPORTATION',
		'OTHERS'
	);
	$partB_questions_1 = array(
							'BUILDINGS'=>array(
									'Efficient use of natural light and ventilation for the buildings.',
									'Building operation and maintenance in terms of energy consumption.',
									'Adaptive reuse instead of demolition of old structures.'
								),
					 		'TRANSPORTATION'=>array(
									'Controlling pollution due to the vehicular movement in the campus.'	
								),
							'WATER'=>array(
									'Management of Treated Water.(Potable water)',
									'Management of waste water(waste from the drains, sewage water etc)',
									'Management of rain water'
								),
							'ENERGY'=>array(
									'Adopting energy efficient appliances such as timers lighting sensors, LED lighting, energy metering etc.',
									'Use of renewable energy resources like solar, wind etc.'
								),
	);
$partB_questions_2 = array(
							'SOLID WASTE'=>array(
									'Waste Management: Waste generation from the offices, domestic waste and Leafy matter etc.',
									'Recycling of the above mentioned waste within the campus.',
									'Reduction of Electronic waste.',
									'Management of hazardous waste i.e. hospital waste ,chemicals from the lab etc'
								),
							'CLIMATE'=>array(
									'Regulating the emissions from solid waste.',
									'Emission due to burning of waste and from the open drains.',
									'Promoting flora to improve the microclimate of the campus'
								),
							'OTHERS'=>array(
									'Increasing the level of community awareness by integrating the environment and sustainability related curriculum, conducting lectures, campaigns, competitions etc.',
									'Community contribution by forming local committee, institution committee, faculty committee',
									'The role of an individual for making campus more sustainable.'
							)
	);
	$partB_options=array(
										1=>'Can\'t Say(CS)',
										2=>'Not at all important(NI)',
										3=>'Somewhat important(SI)',
										4=>'Important(I)',
										5=>'Extremely Important(EI)'
									);
	$partC_questions_1 = array(
							'BUILDINGS'=>array(
									'Efficient use of natural light and ventilation for the buildings.',
									'Building operation and maintenance in terms og energy consumption.',
									'Adaptive reuse instead of demolition of old structures.'
								),
					 	'TRANSPORTATION'=>array(
									'Controlling pollution due to the vehicular movement in the campus.'
								
								),
							'WATER'=>array(
									'Management of Treated Water.(Potable water)',
									'Management of waste water(waste from the drains, sewage water etc)',
									'Management of rain water'
								),
							'ENERGY'=>array(
									'Adopting energy efficient appliances such as timers lighting sensors, LED lighting, energy metering etc.',
									'Use of renewable energy resources like solar, wind etc.'
								),
	);

	$partC_questions_2 = array(
							'SOLID WASTE'=>array(
									'Waste Management: Waste generation from the offices, domestic waste and Leafy matter etc.',
									'Recycling of the above mentioned waste within the campus.',
									'Reduction of Electronic waste.',
									'Management of hazardous waste i.e. hospital waste, chemicals from the lab etc'
								),
							'CLIMATE'=>array(
									'Regulating the emissions from solid waste.',
									'Emission due to burning of waste and from the open drains.',
									'Promoting flora to improve the microclimate of the campus'
								),
							'OTHERS'=>array(
									'Increasing the level of community awareness by integrating the environment and sustainability related curriculum conducting lectures, campaigns, competitions etc.',
									'Community contribution by forming local committee, institution committee, faculty committee',
									'The role of an individual for making campus more sustainable.'
							)
	);
	$partC_options=array(
										1=>'Can\'t Say(CS)',
										2=>'Indequate then and now',
										3=>'Adequate then and inadequate now',
										4=>'Inadequate then and adequate now',
										5=>'Adequate then and now'
									);
	$partD_questions_1 = array(
							'OPENSPACE'=>array(
									'Roads',
									'Playground',
									'Garden/lawns',
									'Vacant/Undeveloped Area'
								),
					 		'MAIN ADMINISTRATION BUILDING'=>array(
									'Directors/Deans Offices/Associate Deans Offices',
									'Associated Offices',
									'Toilets',
									'Canteen'
								),
	);
	$partD_questions_2 = array(
							'DEPARTMENTS'=>array(
									'Department Office',
									'HOD Cabin and P.A',
									'Pantry Area/Tea Room',
									'Conference/Seminar/Meeting/Library Room',
									'Faculty Room',
									'Class Room and research scholar rooms',
									'Labs/computer lab/heavy duty machines',
									'Toilets',
									'Corridors'
								),
							'HOSTELS'=>array(
									'Rooms',
									'Toilets',
									'Office/Warden Room',
									'Common Room/T.V/Clubs/Xerox/parlors/Computer labs',
									'Mess/Canteen',
									'Corridors',
								),
	);
	$partD_questions_3 = array(
							'STAFF ACCOMADATION'=>array(
									'Living',
									'Kitchen',
									'Toilets',
									'Bed Room',
									'Garage/External Space/Garden Space',
									'External Space/Garden Space'
								),
							'HOSPITAL'=>array(
									'Reception/Common Waiting Area',
									'Consulting Rooms/OTs/Office',
									'Wards/Emergency Rooms',
									'Pathology Unit/Dispensary/Pharmacy'
								),
							'OTHERS'=>array(
								'Library',
								'Canteens',
								'Sports Complex',
								'Various clubs like Hobbies Club, Students Club',
								'Common facilities like shops,markets,banks,Post Office,Reservation Counters etc'
							)
	);
	$partD_options=array(
										'ENERGY'=>array(
												1=>'Can\'t Say',
												2=>'Not Important',
												3=>'Important',
												4=>'Extremely Important'
											),
										'WASTE'=>array(
												1=>'Can\'t Say',
												2=>'Not Important',
												3=>'Important',
												4=>'Extremely Important'
											),
										'WATER'=>array(
												1=>'Can\'t Say',
												2=>'Not Important',
												3=>'Important',
												4=>'Extremely Important'
											)
										);
	$partE_questions_1 = array(
							'BUILDINGS'=>array(
									'Efficient land and space use',
									'Efficient new construction',
									'Retrofitting older buildings',
									'Reducing horizontal speed and increasing vertically',
									'Delineating permanant green/forest areas'
								),
					 		'TRANSPORTATION'=>array(
									'Vehicles powered by battery, bio-fuel and solar etc',
									'Public Transport',
									'Use of bicycles',
									'And walking etc',
									'Implementing transportation planning and management policies within the campus'
								),
	);
	$partE_questions_2 = array(
							'OTHERS'=>array(
								'Establishing the sustainability committee',
								'Proper documentation of all activities for knowing better results',
								'Sustainability guidelines at the institution level should be enforced',
								'Investing more funds for sustainability related projects',
								'Comparing more better institutions with other as far as sustainability practice is concerned',
								'Conducting various awareness programme like workshops,seminars,conference related to sustainability issues and practices',
								'Implementing of sustainability focussed courses in regular curriculum',
								'Providing training for students, faculties and staff of the institution',
								'Focussing research also on sustainability aspects.(solar,wind,waste,water,buildings etc)',
								'Promoting and maintaining the flora of the campus',
								'Promoting the use of locally/organically grown edibles like grains,vegetables,fruits',
								'Use of social media to make people aware of sustainability through posters and signages'
							)
	);
	$partE_options=array(
										1=>'Can\'t Say(CS)',
										2=>'It is not relavant',
										3=>'Somewhat relevant',
										4=>'It is relavant'
									);
	$partF_options=array(
										1=>'Yes',
										2=>'No',
									);

?>
