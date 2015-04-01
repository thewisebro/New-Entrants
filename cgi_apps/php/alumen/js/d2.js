function updateInfo(action,mode)
{
	switch(action)
	{
		case "Register":
				loadData('basicForm.php');
				break;
		case "Introduction":
				if(mode==0)
					document.getElementById('middle_left_top').innerHTML=document.getElementById('intro_text').value;
				else
					loadData('introduction.php');
				break;
		case "FullForm":
				loadData('fullForm.php');	
				break;
		case "FullRegisterDone":
				loadData('fullRegisterDone.php');
				break;
		case "SuggestionForm":
				loadData('suggestionForm.php');
				break;
		case "SuggestionSubmittedForm":
				loadData('suggestionSubmittedForm.php');
				break;
		case "ProblemForm":
				loadData('problemForm.php');
				break;
		case "ProblemSubmittedForm":
				loadData('problemSubmittedForm.php');
				break;
		case "ForgotpasswordForm":
				loadData('forgotPasswordForm.php');
				break;	
		case "EditProfileForm":
				loadData('editProfileForm.php');	
				break;
		case "EditProfileDoneForm":		
				loadData('editProfileDoneForm.php');
				break;
		case "ShowProfile":
				loadData('showProfile.php');
				break;
		case "ChangePasswordForm":
				loadData('changePasswordForm.php');
				break;
		case "ChangePasswordDone":
				loadData('changePasswordDone.php');
				break;		
		case "ForgotPasswordForm":

