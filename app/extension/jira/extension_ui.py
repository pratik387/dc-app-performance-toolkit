import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    issue_key = ""

    #General Deployment Request properties
    gen_req_workflow = "MyGeneralWorkflow"
    gen_req_dyn_property_key = "workflow/MyGeneralWorkflow-/MyGeneralWorkflow-/myprop"
    gen_req_dyn_property_val = "50"

    #Application Deployment/Provisioning Request properties
    app_req_application = "DemoApp"
    app_req_workflow = "deploy"
    app_req_package = "test-job10"
    app_req_profile = "Local"
    app_req_dyn_property_key1 = "application/DemoApp-/DemoApp-/dyn_app_prop1"
    app_req_dyn_property_val1 = "app_property"
    app_req_dyn_property_key2 = "components/Backend-/database-/database/database-name"
    app_req_dyn_property_val2 = "db_name_changed"
    app_req_dyn_property_key3 = "components/Backend-/database-/database/database-server"
    app_req_dyn_property_val3 = "db_server_changed"

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    
    @print_timing("selenium_app_specific_user_login")
    def measure():
        
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.set_credentials(username=username, password=password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')

        @print_timing("selenium_app_custom_create_issue: general_deployment_request")
        def sub_measure():
            time.sleep(2)
            page.wait_until_clickable((By.ID, "create_link")).click()
            
            time.sleep(2)
            page.wait_until_clickable((By.ID , "project-field")).click()
            page.get_element((By.ID , "project-field")).send_keys(Keys.BACKSPACE)
            page.get_element((By.ID , "project-field")).send_keys("Selenium_Test_project")
            page.wait_until_visible((By.ID , "project-field")).send_keys(Keys.TAB)
            
            time.sleep(2)
            page.wait_until_clickable((By.ID , "issuetype-field")).click()
            page.get_element((By.ID , "issuetype-field")).send_keys(Keys.BACKSPACE)
            page.wait_until_visible((By.ID , "issuetype-field")).send_keys("General Deployment Request")
            page.wait_until_visible((By.ID , "issuetype-field")).send_keys(Keys.TAB)
            
            time.sleep(2)
            page.wait_until_clickable((By.ID, "summary")).send_keys("gen_req_issue_test")
            # time.sleep(2)
            page.wait_until_visible((By.ID, "create-issue-submit")).click()
            
        sub_measure()

        @print_timing("selenium_app_custom_action:execute_issue:general_deployment_request")
        def sub_measure():
             global issue_key
             issue_key = page.wait_until_visible((By.CLASS_NAME, "issue-created-key")).get_attribute("data-issue-key")
             page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
             page.wait_until_visible((By.ID, "summary-val"))   
             page.wait_until_visible((By.ID, "validation-web-item-link"))  
             page.wait_until_visible((By.ID, "validation-web-item-link")).click()
            
             page.wait_until_visible((By.ID, "rmWorkflow"))
             page.select(page.get_element((By.ID, "rmWorkflow"))).select_by_visible_text(gen_req_workflow)
             
             time.sleep(2)
             page.wait_until_clickable((By.ID, "rmNow")).click()
             page.wait_until_visible((By.ID, "rmPrompt")).click()
             page.wait_until_visible((By.ID, gen_req_dyn_property_key)).click()
             page.wait_until_visible((By.ID, gen_req_dyn_property_key)).send_keys((Keys.CONTROL, 'a'), gen_req_dyn_property_val);
             page.wait_until_visible((By.ID, "rmSave")).click()
             page.wait_until_visible((By.ID, "action_id_21")).click()
             page.wait_until_visible((By.ID, "issue-workflow-transition-submit")).click()
             #verify the button Failed2StartExecution visible after execution starts
             page.wait_until_visible((By.ID, "action_id_31"))

        sub_measure()

        @print_timing("selenium_app_custom_action:view_issue:general_deployment_request")
        def sub_measure():
            global issue_key
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            time.sleep(1)
            ele = page.wait_until_visible((By.XPATH, "//span[@id='status-val']/span")).text

            if "CLOSED" == ele:
                print("Execution complete")
            elif "EXECUTING IN CDA" == ele:
                print("executing in CDA")
            else:
                assert "CLOSED" == ele
        sub_measure()

        @print_timing("selenium_app_custom_create_issue:application_deployment/provisioning_request")
        def sub_measure():
            time.sleep(2)
            page.wait_until_clickable((By.ID, "create_link")).click()
            time.sleep(2)
            page.wait_until_clickable((By.ID , "project-field")).click()
            page.get_element((By.ID , "project-field")).send_keys(Keys.BACKSPACE)
            page.wait_until_visible((By.ID , "project-field")).send_keys("Selenium_Test_project")
            page.wait_until_visible((By.ID , "project-field")).send_keys(Keys.TAB)
            time.sleep(2)
            page.wait_until_clickable((By.ID , "issuetype-field")).click()
            page.get_element((By.ID , "issuetype-field")).send_keys(Keys.BACKSPACE)
            page.wait_until_visible((By.ID , "issuetype-field")).send_keys("Application Deployment/Provisioning Request")
            page.wait_until_visible((By.ID , "issuetype-field")).send_keys(Keys.TAB)
            time.sleep(2)
            page.wait_until_clickable((By.ID, "summary")).send_keys("app_dep_req_issue_test")
            page.wait_until_visible((By.ID, "create-issue-submit")).click()
            
        sub_measure()

        @print_timing("selenium_app_custom_action:execute_issue:application_deployment/provisioning_request")
        def sub_measure():
            global issue_key
            issue_key = page.wait_until_visible((By.CLASS_NAME, "issue-created-key")).get_attribute("data-issue-key")
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))
            page.wait_until_visible((By.ID, "validation-web-item-link"))  
            page.wait_until_visible((By.ID, "validation-web-item-link")).click()
            
            page.wait_until_visible((By.ID, "rmApplication"))
            page.select(page.get_element((By.ID, "rmApplication"))).select_by_visible_text(app_req_application)
            
            page.wait_until_visible((By.ID, "rmWorkflow"))
            page.select(page.get_element((By.ID, "rmWorkflow"))).select_by_visible_text(app_req_workflow)
            
            page.wait_until_visible((By.ID, "rmPackage"))
            page.select(page.get_element((By.ID, "rmPackage"))).select_by_visible_text(app_req_package)
            
            page.wait_until_visible((By.ID, "rmProfile"))
            page.select(page.get_element((By.ID, "rmProfile"))).select_by_visible_text(app_req_profile)
            
            time.sleep(2)
            page.wait_until_clickable((By.ID, "rmNow")).click()
            page.wait_until_visible((By.ID, "rmPrompt")).click()
            page.wait_until_visible((By.ID, app_req_dyn_property_key1)).click()
            page.wait_until_visible((By.ID,app_req_dyn_property_key1)).send_keys((Keys.CONTROL, 'a'), app_req_dyn_property_val1)
            page.wait_until_visible((By.ID, app_req_dyn_property_key2)).click()
            page.wait_until_visible((By.ID, app_req_dyn_property_key2)).send_keys((Keys.CONTROL, 'a'), app_req_dyn_property_val2)
            page.wait_until_visible((By.ID, app_req_dyn_property_key3)).click()
            page.wait_until_visible((By.ID, app_req_dyn_property_key3)).send_keys((Keys.CONTROL, 'a'), app_req_dyn_property_val3)
            page.wait_until_visible((By.ID, "rmSave")).click()
            page.wait_until_visible((By.ID, "action_id_21")).click()
            page.wait_until_visible((By.ID, "issue-workflow-transition-submit")).click()
            
            #verify the button Failed2StartExecution visible after execution starts
            page.wait_until_visible((By.ID, "action_id_31"))
            

        sub_measure()

        @print_timing("selenium_app_custom_action:view_issue:application_deployment/provisioning_request")
        def sub_measure():
            global issue_key
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))
            time.sleep(1)
            ele = page.wait_until_visible((By.XPATH, "//span[@id='status-val']/span")).text
            if "CLOSED" == ele:
                print("Execution complete")
            elif "EXECUTING IN CDA" == ele:
                print("executing in CDA")
            else:
                assert "CLOSED" == ele
        sub_measure()
    measure()
