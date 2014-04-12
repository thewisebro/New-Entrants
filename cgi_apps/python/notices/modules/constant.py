"""
All Categories and Sub-Categories are mentioned in this file
and mentioned nowhere else
Hence If u have to add a sub-category or category you have to make changes 
in this file.
To add a subactegory make changes in <Category> dict and <Category>_order list
(dict are unordered that's why <Category>_order list(which are ordered) is made)
"""



NoticesUrlBase="http://192.168.121.6/Notices/"

Categories=["Placement","Authorities","Bhawans","Departments"]

Authorities={
"acad":"Academics",
"cpo":"CPO",
"dosw":"DOSW",
"alumni":"Alumni Affairs",
"cnst":"Construction",
"clib":"Central Library",
"cd":"CD",
"dean":"Deans",
"hod":"Heads",
"hspl":"Hospital",
"rgst":"Registrar",
"finc":"Finance",
"pstd":"Ps to Director",
"stdd":"Steno to Deputy Director",
"qip":"QIP",
"snt":"Senate",
"isc":"ISC"}
Authorities_order=["acad","cpo","dosw","alumni","cnst","clib","cd","dean","hod","hspl","rgst","finc",\
                    "pstd","stdd","qip","snt","isc"]
Bhawans={
"azd":"Azad",
"ctl":"Cautley",
"gng":"Ganga",
"gvnd":"Govind",
"jwhr":"Jawahar",
"rjnd":"Rajendra",
"rvnd":"Ravindra",
"srjn":"Sarojini",
"kstr":"Kasturba",
"mlvy":"Malviya",
"rjv":"Rajeev",
"rkb":"Radhakrishnan"}
Bhawans_order=["azd","ctl","gng","gvnd","jwhr","rjnd","rvnd","srjn","kstr","mlvy","rjv","rkb"]

Departments={
"ahec":"Alternative Hydro Energy Centre",
"arch":"Architecture and Planning",
"bt":"Biotechnology",
"chem":"Chemical",
"cvl":"Civil",
"cy":"Chemistry",
"erts":"Earth-Science",
"ertq":"Earthquake",
"ee":"Electrical",
"ec":"Electronics and Computer Science",
"hydr":"Hydrology",
"hs":"Humanities",
"dpt":"DPT",
"ms":"Management Studies",
"ma":"Mathematics",
"mi":"Mechanical and Industrial",
"meta":"Metallurgy",
"ph":"Physics",
"wtr":"Water Resources Development and Management",
"icc":"Institute Computer Centre",
}
Departments_order=["ahec","arch","bt","chem","cvl","cy","erts","ertq","ee","ec",\
                   "hydr","hs","dpt","ms","ma","mi","meta","ph","wtr","icc"]


Placement={
"po":"Placement Office"}
Placement_order=["po"]

