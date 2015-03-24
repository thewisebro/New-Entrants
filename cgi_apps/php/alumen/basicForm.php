
<span class="header">Step 1 of 2: Register to be a Mentor!</span>
<form method="post" action="basicRegister.php" enctype="multipart/form-data" onsubmit="return checkForm(this);">
<br/>
<span class="header">*</span> marked fields are mandatory.
<table border="0">
	<tr>
	<td>Username</td>
 	<td><input name="username"  type="text"><span class="header">*</span><span id="form_tips">6-10 characters [a-z,0-9,_]</span></td>
	</tr>
	
	<tr>
	<td>Password </td>
 	<td><input name="password"  type="password"><span class="header">*</span><span id="form_tips">5-10 characters [a-z,A-Z,0-9]</span></td>
	</tr>
	
	<tr>
	<td>Retype Password </td>
 	<td><input  name="repassword" type="password"><span class="header">*</span></td>
	</tr>

	<tr>
	<td>Full name </td>
 	<td><input name="fullname"  type="text"><span class="header">*</span></td>
	</tr>
	
	<tr>
	<td>Email </td>
 	<td><input name="email"  type="text"><span class="header">*</span><br/><span id="form_tips">Your email address will only be used by the administrator to contact you. It will not be made available to students participating in the programme without your consent.</span>
		</td>
	</tr>

	<tr>
	<td>Year of Passing</td>
	<td><input type="text" name="passing_year" maxlength="4"><span class="header">*</span></td>
	</tr>	

	<tr>
	<td>Department</td>
	<td>
		<select name="department" size="1" id="department"> 
		<option value="" selected="selected">Select...</option>
		<option value="AHEC">AHEC</option>

                <option value="AP">Architecture </option>
                <option value="BT">Biotechnology</option>
                <option value="CY">Chemical Engineering</option>
                <option value="CH">Chemistry</option>
                <option value="CE">Civil Engineering</option>
                <option value="EQ">Earthquake</option>
                <option value="ES">Earth Sciences</option>
                <option value="EE">Electrical Engineering</option>
                <option value="ECE">Electronics &amp; Computer Engineering</option>
                
                <option value="HS">Humanities</option>
                <option value="HY">Hydrology</option>
                <option value="BM">Management Studies</option>
                <option value="MA">Mathematics</option>
                <option value="MI">Mechanical &amp; Industrial Engineering</option>
                <option value="MT">Metallurgical and Material Engineering</option>
                <option value="PP">Paper. &amp; Pulp Engineering</option>
                
                <option value="PH">Physics</option>
                <option value="WR">Water Resources</option>
                <option value="OT">Others</option>
		</select><span class="header">*</span>
	</td>
	</tr>
	
	<tr>
		<td>Degree</td>
		<td>
		       <select name="degree" size="1" id="degree">
		       		<option value=""  selected="selected">Select...</option>
                       		<option value="B. Tech." >B.Tech.</option> 
                       		<option value="B. Tech. Dual" >B.Tech. Dual</option> 
		       		<option value="B. Arch.">B.Arch.</option> 
                       		<option value="M. Tech.">M.Tech.</option>
                       		<option value="M. Sc.">M.Sc.</option> 
                       		<option value="Ph.D.">Ph.D.</option> 
                       		<option value="M.B.A.">M.B.A.</option>
                       		<option value="M.C.A.">M.C.A.</option>
                    		<option value="Other">Other</option> 
                        </select><span class="header">*</span> 	
                 </td>
	</tr>
	<tr>
		<td>Enrollment Number</td>
		<td> <input type="text" name="enrollment_no"></td>
	</tr>
	<tr>
		<td>Upload your recent photograph</td>
		<td> <input type="file" name="photo"><span id="form_tips">(only JPEG with maximum size limit of 25kB allowed)</span></td>
	</tr>
	<tr>
	<td>
	<input type="hidden" id="notSubmit" value="1">
	<br/>
	<br/>
<input type="submit" value="Register" name="basic_login" onclick="document.getElementById('notSubmit').value=0">
	</td>
	<td></td>
	</tr>
</table>	
<p><b>Privacy Statement:</b> The administrator of this portal will make all possible efforts to ensure that your contact details are neither displayed nor made available to any person without your knowledge and consent. However, the administrator and or the institute can not be held legally responsible for inadvertent misuse.</p>	

</form>
<br/>
<a href="#ProblemForm" onclick="updateInfo('ProblemForm',1)"><span class="header">Problems in Registration?</span><a/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
