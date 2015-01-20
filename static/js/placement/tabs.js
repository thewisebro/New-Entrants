document.onclick = clicked;

if (window.addEventListener) // W3C standard
{
    window.addEventListener('load', loaded, false); // NB **not** 'onload'
}
else if (window.attachEvent) // Microsoft
{
    window.attachEvent('onload', loaded);
}


function loaded(){
    var path = location.pathname;
    var node = false;
    switch(true){
  		case (path.match('placement/$') != null):
          node = document.getElementById("home_li");
		    	break;
  		case (path.indexOf("personal_information") != -1):
          node = document.getElementById("personal_information_li");
		    	break;
  		case (path.indexOf("photo") != -1):
          node = document.getElementById("photo_li");
		    	break;
  		case (path.indexOf("contact") != -1):
          node = document.getElementById("contact_li");
		    	break;
			case (path.indexOf("educational_details") != -1):
		      node = document.getElementById("educational_details_li");
		    	break;
			case (path.indexOf("placement_information") != -1):
		      node = document.getElementById("placement_information_li");
		    	break;
			case (path.indexOf("internship_information") != -1):
		      node = document.getElementById("internship_information_li");
		    	break;
			case (path.indexOf("extra_curriculars") != -1):
		      node = document.getElementById("extra_curriculars_li");
		    	break;
			case (path.indexOf("languages_known") != -1):
		      node = document.getElementById("languages_known_li");
		    	break;
			case (path.indexOf("job_experiences") != -1):
		      node = document.getElementById("job_experiences_li");
		    	break;
			case (path.indexOf("project_information") != -1):
		      node = document.getElementById("project_information_li");
		    	break;
			case (path.indexOf("research_publications") != -1):
		      node = document.getElementById("research_publications_li");
		    	break;
			case (path.indexOf("branches") != -1):
		      node = document.getElementById("branches_li");
		    	break;
			case (path.indexOf("upload_form") != -1):
		      node = document.getElementById("upload_form_li");
		    	break;
			case (path.indexOf("cpt") != -1):
		      node = document.getElementById("cpt_members_li");
		    	break;
			case (path.indexOf("secondround") != -1):
		      node = document.getElementById("second_round_li");
		    	break;
			case (path.indexOf("results") != -1):
		      node = document.getElementById("results_li");
		    	break;
			case (path.indexOf("technical_forum") != -1):
		      node = document.getElementById("technical_forum_li");
		    	break;
			case (path.indexOf("placement_forum") != -1):
		      node = document.getElementById("placement_forum_li");
		    	break;
			case (path.indexOf("feedbacks") != -1):
		      node = document.getElementById("feedbacks_li");
		    	break;
			case (path.indexOf("downloads") != -1):
		      node = document.getElementById("download_statistics_li");
		    	break;
			case (path.indexOf("all_departments") != -1):
		      node = document.getElementById("all_departments_li");
		    	break;
			case (path.indexOf("company/list") != -1):
		      node = document.getElementById("company_list_li");
		    	break;
			case (path.indexOf("results/branch") != -1):
		      node = document.getElemenotById("results_li");
		    	break;
			case (path.indexOf("notices/upload") != -1):
		      node = document.getElementById("upload_form_li");
		    	break;
			case (path.indexOf("notices") != -1):
		      node = document.getElementById("forms_li");
		    	break;
			case (path.indexOf("sample/resume") != -1):
		      node = document.getElementById("sample_resume_li");
		    	break;
			case (path.indexOf("sample/papers.zip") != -1):
		      node = document.getElementById("sample_papers_li");
		    	break;
			case (path.indexOf("branch") != -1):
		      node = document.getElementById("student_details_li");
		    	break;
			case (path.indexOf("forum/T") != -1):
		      node = document.getElementById("technical_forum_li");
		    	break;
			case (path.indexOf("forum/P") != -1):
		      node = document.getElementById("placement_forum_li");
		    	break;
			case (path.indexOf("FAQ") != -1):
		      node = document.getElementById("faq_li");
		    	break;
			case (path.indexOf("feedback") != -1):
		      node = document.getElementById("feedbacks_li");
		      break;
  		case (path.match('facapp/$') != null):
          node = document.getElementById("home_li");
		    	break;
  		case (path.match('add/EducationalDetails') != null):
          node = document.getElementById("educational_details_li");
		    	break;
  		case (path.match('update/Faculty/1') != null):
          node = document.getElementById("general_information_li");
		    	break;
  		case (path.match('add/AdministrativeBackground/') != null):
          node = document.getElementById("administrative_background_li");
		    	break;
  		case (path.match('add/Honors') != null):
          node = document.getElementById("honors_li");
		    	break;
  		case (path.match('add/Membership') != null):
          node = document.getElementById("membership_li");
		    	break;
  		case (path.match('add/ProfessionalBackground') != null):
          node = document.getElementById("professional_background_li");
		    	break;
  		case (path.match('add/ParticipationSeminar') != null):
          node = document.getElementById("participation_seminar_li");
		    	break;
  		case (path.match('add/Miscellaneous') != null):
          node = document.getElementById("miscellaneous_li");
		    	break;
  		case (path.match('add/Collaboration') != null):
          node = document.getElementById("collaboration_li");
		    	break;
  		case (path.match('add/Invitations') != null):
          node = document.getElementById("invitations_li");
		    	break;
  		case (path.match('add/MultiplePost') != null):
          node = document.getElementById("multiple_posts_li");
		    	break;
  		case (path.match('add/TeachingEngagement') != null):
          node = document.getElementById("teaching_engagements_li");
		    	break;
  		case (path.match('add/SponsoredResearchProjects') != null):
          node = document.getElementById("sponsored_research_projects_li");
		    	break;
  		case (path.match('add/ProjectAndThesisSupervision') != null):
          node = document.getElementById("project_and_thesis_supervision_li");
		    	break;
  		case (path.match('add/PhdSupervised') != null):
          node = document.getElementById("phd_supervised_li");
		    	break;
  		case (path.match('add/ResearchScholarGroup') != null):
          node = document.getElementById("research_scholar_group_li");
		    	break;
  		case (path.match('add/Interests') != null):
          node = document.getElementById("interests_li");
		    	break;
  		case (path.match('add/Visits') != null):
          node = document.getElementById("visits_li");
		    	break;
  		case (path.match('add/ParticipationInShorttermCourses') != null):
          node = document.getElementById("participation_short_term_courses_li");
		    	break;
  		case (path.match('add/OrganisedConference') != null):
          node = document.getElementById("organised_conference_li");
		    	break;
  		case (path.match('add/SpecialLecturesDelivered') != null):
          node = document.getElementById("special_lectures_delivered_li");
		    	break;
  		case (path.match('books_authored') != null):
          node = document.getElementById("books_authored_li");
		    	break;
  		case (path.match('refereed_journal_papers') != null):
          node = document.getElementById("refreed_journal_papers_li");
		    	break;
  		case (path.match('mass_mailer') != null):
          node = document.getElementById("mass_mailer_li");
		    	break;
      default:
          node = false;
    }
    
    if(node)
        node.style.cssText = 'background:#c2c2c2;';
}

function clicked(ev){
    ev = ev || window.event;
    var node = ev.target || ev.srcElement;
    if(node.id == "tab_1_heading"){
        node.style.cssText = 'background:#e3e3e3;';
        var other_node = document.getElementById("tab_2_heading");
        other_node.style.cssText = 'background:#FFFFFF;';
    }
    else if(node.id == "tab_2_heading"){
        node.style.cssText = 'background:#e3e3e3;';
        var other_node = document.getElementById("tab_1_heading");
        other_node.style.cssText = 'background:#FFFFFF;';
    }
    else if(node.nodeName == "LI"){
        /* Do not do anything as the above selection is highlighting every LI */
        /* node.style.cssText = 'background:#c2c2c2;'; */
    }
}
