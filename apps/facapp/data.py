
################################################ add "add new" field for relevant sections ####################################
############################################## add appropriate choices for select tag inputs ##################################

titles = [
	"Educational Details",
	"General Information",
	"Administrative Background",
	"Honors",
	"Membership",
	"Professional Background",
	"Participation Seminar",
	"Miscellaneous",
	"Collaboration",
	"Invitations",
	"Multiple Posts",
	"Teaching Engagements",
	"Sponsored Research Projects",
	"Project And Thesis Supervision",
	"Phd Supervised",
	"Research Scholar Group",
	"Areas Of Interests",
	"Visits",
	"Participation In Short Term Courses",
	"Organised Conference",
	"Special Lectures Delivered",
	"Books Authored",
	"Referred Journal Papers",
	"Upload Website",
	"FacSpace",
]

data = [
	(
		["title", "General Information"],
		["showAlways", "True"],
		["inputs", (
			["Name", "readonly"],
			["Department", "readonly"], # prof doesnt have rights to change this field.
			["Photo", "uploadPhoto"],
			["Resume", "uploadPdf"],
			["Designation", "select"],
			["Date Of Birth","text"],
			["Phone Number", "text"],
			["Address", "text"],
			["Alternate mail id", "text"],
			############################################### add more fields here ############################################
			),
		],
	),
	(
		["title", "Educational Details"],
		["showAlways", "True"],
		["inputs", (
			["Subject", "text"],
			["Year", "text"],
			["University", "text"],
			["Degree", "text"],
			# ["Visibility","checkbox"], ################### add this field to all sections ? ################################
			),
		],
	),
	(
		["title", "Administrative Background"],
		["showAlways", "False"],
		["inputs", (
			["From Year", "text"],
			["To Year", "text"],
			["Designation", "text"],
			["Organisation", "text"],
			["At Level", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Honors"],
		["showAlways", "True"],
		["inputs", (
			["Year", "text"],
			["Award", "text"],
			["Institute", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Membership"],
		["showAlways", "False"],
		["inputs", (
			["Organisation", "text"],
			["Position", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Professional Background"],
		["showAlways", "True"],
		["inputs", (
			["From Year", "text"],
			["To Year", "text"],
			["Designation", "text"],
			["Organisation", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Participation Seminar"],
		["showAlways", "False"],
		["inputs", (
			["Name", "text"],
			["Place", "text"],
			["Sponsored by", "text"],
			["Date", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Miscellaneous"],
		["showAlways", "False"],
		["inputs", (
			["Particulars of course", "textarea"],
			["Innovation in teaching", "textarea"],
			["Instructional tasks", "textarea"],
			["Process Development", "textarea"],
			############################################### add more fields here ############################################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Collaboration"],
		["showAlways", "False"],
		["inputs", (
			["Topic", "textarea"],
			["Organisation", "text"],
			["Level", "select"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Invitations"],
		["showAlways", "False"],
		["inputs", (
			["Topic", "textarea"],
			["Organisation", "text"],
			["Category", "select"],
			["Year", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Multiple Posts"],
		["showAlways", "False"],
		["inputs", (
			["Post", "textarea"],
			############################################### what is this ? ######################################################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Teaching Engagements"],
		["showAlways", "True"],
		["inputs", (
			["Class Name", "text"],
			["course code", "text"],
			["Semester", "text"],
			["Title", "text"],
			["Number of students", "text"],
			["Lecture hours", "text"],
			["Practical hours", "text"],
			["Tutorial hours", "text"],
			["", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Sponsored Research Projects"],
		["showAlways", "False"],
		["inputs", (
			["Financial outlay", "text"],
			["Funding agency", "text"],
			["Period", "text"],
			["Other investigating officer", "text"],
			["Status of project", "select"],
			["Type of project", "select"],
			["Year", "text"],
			["Topic", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Project and Thesis Supervision"],
		["showAlways", "True"],
		["inputs", (
			["Title of Project", "text"],
			["Name of students", "textarea"],
			["Name of other supervisor(s)", "text"],
			["Description", "textarea"],
			["Course", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Phd Supervised"],
		["showAlways", "True"],
		["inputs", (
			["Topic", "text"],
			["Name of other supervisor(s)", "text"],
			["Registration year", "text"],
			["Status of Phd", "select"],
			["Phd type", "select"],
			["Scholar name", "text"],
			############################################### check if scholar name should be kept above ############################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Research Scholar Group"],
		["showAlways", "False"],
		["inputs", (
			["Scholar name", "text"],
			["Interest", "text"],
			["Home page", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Areas Of Interests"],
		["showAlways", "True"],
		["inputs", (
			["General topic", "text"],
			["Research Work topic", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Visits"],
		["showAlways", "False"],
		["inputs", (
			["Purpose of visit", "textarea"],
			["Institute visited", "text"],
			["Date", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Participation In Short-term Courses"],
		["showAlways", "False"],
		["inputs", (
			["Course name", "text"],
			["Sponsored by", "text"],
			["Date", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Organised Conference"],
		["showAlways", "False"],
		["inputs", (
			["Conference name", "text"],
			["Sponsored by", "text"],
			["Date", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Special Lectures Delivered"],
		["showAlways", "False"],
		["inputs", (
			["Title", "text"],
			["Place", "text"],
			["Description", "textarea"],
			["Date", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Books Authored"],
		["showAlways", "False"],
		["inputs", (
			["Name of book", "text"],
			["Topic/Subject", "text"],
			############################################ add more inputs maybe ##################################################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "Referred Journal Papers"],
		["showAlways", ""],
		["inputs", (
			["", "text"],
			["", "text"],
			["", "text"],
			["", "text"],
			############################################ add more inputs maybe ##################################################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "UPload Website"],
		["showAlways", ""],
		["inputs", (
			["", "text"],
			["", "text"],
			["", "text"],
			["", "text"],
			############################################ add more inputs maybe ##################################################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", "FacSpace"],
		["showAlways", ""],
		["inputs", (
			["", "text"],
			["", "text"],
			["", "text"],
			["", "text"],
			############################################ add more inputs maybe ##################################################
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", ""],
		["showAlways", ""],
		["inputs", (
			["", "text"],
			["", "text"],
			["", "text"],
			["", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),
	(
		["title", ""],
		["showAlways", ""],
		["inputs", (
			["", "text"],
			["", "text"],
			["", "text"],
			["", "text"],
			# ["Visibility", "checkbox"],
			),
		],
	),

]