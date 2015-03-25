<select name="industry" onChange="if(document.registerForm.industry.options[selectedIndex].value=='-1'){document.getElementById('other_ind').style.display='inline';document.getElementById('ind_spl').style.display='none';} else {document.getElementById('ind_spl').style.display='inline';document.getElementById('other_ind').style.display='none'}">
<option value="">-- Select an Industry --</option>
<option value="200">Automobiles</option>
<option value="300">Chemicals, Metals, Papers, Other Materials</option>
<option value="500">Construction, Building</option>
<option value="1600">Consulting, Legal, Engineering, Accounting</option>
<option value="400">Consumer Goods, Consumer Services</option>
<option value="600">Education</option>
<option value="700">Energy, Oil, Gas</option>
<option value="800">Federal, State, Local Governments</option>
<option value="900">Financial Services, Banks, Credit Unions</option>
<option value="1000">Healthcare, Pharmaceuticals, Life Sciences, Biotechnology</option>
<option value="1200">Heavy Machinery, Industrial Markets, Defense</option>
<option value="1100">Hotels, Restaurants, Clubs, Other Leisure</option>
<option value="1300">Information Technology, Software, Hardware, Electronics</option>
<option value="1400">Media, Advertising, Publishing, Entertainment</option>
<option value="1500">Non-profit, Social Sector</option>
<option value="1700">Real Estate, Insurance</option>
<option value="1800">Retail, Wholesale</option>
<option value="1900">Telecommunications</option>
<option value="100">Transportation, Rail, Road, Air, Marine</option>
<option value="-1">Other</option>
</select>
<br/>
<br/>
<input type="text" name="ind_spl" id="ind_spl" value="Area Of Specialization" style="display:none">
<input type="text" name="other_ind" id="other_ind" value="Please Specify" style="display:none">

