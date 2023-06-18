# student-attendance-AI
# Planning:

every day at 7 PM

Deliverable:

Team's strength points:

Ahmad Iraqi: leadership, teamwork 

Mohammad Shareef: frontend, teamwork

Mohmmad Smadi: backend, database

Alaa Hmaidat: design, documentation

Salah Hammash: testing, teamwork




# Conflict Plan:

1. Resolving Conflict:
   - Encourage open communication: Create an environment where team members feel comfortable expressing their concerns and opinions.
   - Active listening: Ensure that all parties involved have an opportunity to share their perspectives without interruption.
   - Identify common goals: Focus on shared objectives and remind team members of the larger project vision.
   - Collaborative problem-solving: Encourage brainstorming and finding mutually acceptable solutions.
   - Mediation: If necessary, appoint a neutral party to facilitate the resolution process and ensure fairness.

2. Dominant Team Member:
   - Facilitate equal participation: Establish clear roles and responsibilities to distribute tasks among team members.
   - Open dialogue: Address the issue directly with the dominant team member, expressing the need for everyone to contribute and share ideas.
   - Encourage rotation: Implement a rotation system for leadership or task ownership, ensuring everyone gets an opportunity to take charge.

3. Handling Different Skill Levels:
   - Foster a learning environment: Promote knowledge sharing and provide resources or training opportunities to help bridge skill gaps.
   - Peer support: Encourage collaboration and peer mentoring, where team members with more expertise can assist others.
   - Clearly defined expectations: Set clear objectives and communicate expectations for each team member, taking into account their individual skill levels.

4. Addressing Inadequate Contribution:
   - Private conversation: Approach the individual privately and express concerns about their contribution to the project.
   - Seek understanding: Understand any potential reasons behind their inadequate contribution and offer support or guidance if needed.
   - Set specific goals: Collaboratively establish specific targets for improvement and regular check-ins to track progress.

5. Escalating Conflicts:
   - Use internal channels first: If resolution attempts fail, involve a supervisor or project manager within the team structure to mediate or provide guidance.
   - Formal grievance procedure: If internal resolution isn't possible, follow any established protocols or escalation paths within your organization.
   - Seek external help if necessary: In extreme cases, involve HR or seek external mediation to address and resolve the conflict impartially.

Remember, the specific approach may vary depending on the team dynamics, organizational culture, and the severity of the conflict. It's essential to adapt these guidelines to your specific situation.




# Communication Plan:
we will be available to communicate between 11 AM and 10 PM
we will use WhatsApp and Slack
whenever is needed 
help each other
we will use WhatsApp and Slack every time we need each other
give each one a space to talk and express his idea about anything
listen to each other with respect 
Git Process:
we will inform all the team members whenever someone wants to push or pull on the repo.moreover, all members will review each others work


# User Stories
Title: User Login
User Story Sentence: As a registered user, I want to be able to log in to my account to access the platform's features and functionalities.
Feature Tasks:
1. Implement a login form with fields for username/email and password.
2. Validate user inputs for correct formatting and required fields.
3. Verify the user's credentials against the stored user information in the database.
4. Provide appropriate feedback to the user upon successful login.
5. Store session or authentication tokens to keep the user logged in during their browsing session.

Acceptance Tests:
1. Enter valid login credentials and ensure successful authentication and redirection to the user's dashboard or main page.
2. Attempt login with incorrect credentials and verify appropriate error messages are displayed.
3. Test the login process with both username and email options to ensure both work correctly.
4. Check that the user remains logged in when navigating through different pages or performing actions within the platform.
5. Log out from the user account and confirm that the user is successfully logged out and redirected to the login page.

Title: Create a Task
User Story Sentence: As a user, I want to be able to create a task and provide essential details for tracking my work.
Feature Tasks:
1. Design and implement a task creation form with fields for title, description, and due date.
2. Validate user inputs for required fields and appropriate formatting.
3. Store the created task in the database, associating it with the user's account.
4. Display the created task in the user's task list or dashboard.
5. Provide confirmation or feedback to the user upon successful task creation.

Acceptance Tests:
1. Fill in the task creation form with all required details and verify that the task is successfully created and saved in the database.
2. Attempt to create a task without providing the required information and ensure appropriate error messages are displayed.
3. Check that the created task appears in the user's task list or dashboard, displaying the correct details.
4. Edit the created task and confirm that the changes are saved and reflected in the task details.
5. Delete the task and verify that it is removed from the user's task list or dashboard.

Title: View Task Details
User Story Sentence: As a user, I want to be able to view the details and status of a task to understand its requirements and progress.
Feature Tasks:
1. Implement a task details page or modal to display task-specific information.
2. Show the task's title, description, due date, assigned user, and status.
3. Provide an option to view additional details or comments related to the task.
4. Allow the user to navigate back to the task list or dashboard after viewing the task details.

Acceptance Tests:
1. Click on a task from the task list or dashboard and ensure that the task details page/modal opens.
2. Verify that the task details page/modal displays the correct title, description, due date, assigned user, and status.
3. Test the functionality to view additional details or comments related to the task and ensure they are displayed correctly.
4. Navigate back to the task list or dashboard from the task details page/modal and confirm that the user is returned to the previous view.

Title: Update Task Status
User Story Sentence: As a user, I want to be able to update the status of a task to reflect its progress or completion.
Feature Tasks:
1. Provide a visual representation or selection options for task status (e.g., "In Progress," "Completed," "Pending," etc.).
2. Allow the user to change the status of a task by selecting the appropriate option.
3. Update the task's status in the database and reflect the change in the user's task list or dashboard.
4. Provide feedback or confirmation to the user upon successful status update
# Software Requirements
[requirements](./requirements.md)
# Domain Modeling
Entities:
1. Student
   - Properties:
     - ID (int)
     - Name (string)
     - FaceImage (image or byte array)
     - AttendanceRecords (list of AttendanceRecord)

2. AttendanceRecord
   - Properties:
     - ID (int)
     - Student (Student)
     - Timestamp (datetime)

Relationships:
- Each Student can have multiple AttendanceRecords (one-to-many relationship)
- Each AttendanceRecord is associated with one Student (many-to-one relationship)

Functions/Methods:
1. Student Registration
   - registerStudent(name: string, faceImage: image or byte array): Student

2. Face Recognition
   - recognizeFace(faceImage: image or byte array): Student

3. Attendance Recording
   - recordAttendance(student: Student): AttendanceRecord

4. Attendance Retrieval
   - getAttendanceRecords(student: Student): AttendanceRecord[]

# Using a Database
There's no database yet

