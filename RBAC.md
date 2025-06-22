### 1\. Understanding Permission Granularity

Permissions can be defined at different levels:

  * **Module Level:** Access to an entire section (e.g., "Payroll Management").
  * **Feature Level:** Access to specific features within a module (e.g., "Payslip Generation").
  * **Action Level:** Granular control over actions (Create, Read, Update, Delete - CRUD).

For your HRMS, we'll primarily focus on **Module and Action Level** permissions.

-----

### 2\. Core Roles and Their Detailed Access

Let's define the key roles in your HRMS and their respective permissions:

#### 2.1. Admin Role

The **Admin** role is the superuser with full control over the entire application.

  * **Access Level:** All modules, all features, all actions (CRUD) across the entire system.
  * **Specific Permissions:**
      * **User Management:** Create, Read, Update, Delete users and assign roles.
      * **System Configuration:** Manage system settings, environment profiles, audit logs.
      * **All Core HR Functions:** Full CRUD access to Employee Information, Payroll, Time & Attendance, Recruitment, Performance, Learning, Benefits, Reporting, Employee Self-Service, Manager Self-Service.
      * **All Advanced Features:** Full CRUD access to Talent Management, Expense Management, Document Management, Compliance Management.
      * **Data Export/Import:** Unrestricted access to all data export and import functionalities.
      * **Audit Logs:** View all system audit logs.

#### 2.2. HR Role

The **HR** role is responsible for managing all human resources-related processes and employee data.

  * **Access Level:** Comprehensive access to HR-specific modules.
  * **Specific Permissions:**
      * **Employee Information Management:**
          * **Create:** Add new employee records.
          * **Read:** View all employee records and detailed information.
          * **Update:** Modify existing employee records (contact, job roles, employment history).
          * **Delete:** Remove employee records (with proper confirmation/soft delete).
      * **Payroll Management:**
          * **Create:** Set up new salary structures, define pay cycles.
          * **Read:** View all payroll data, payslips, tax, and deduction rules.
          * **Update:** Modify salary details, tax, and deduction rules.
          * **Generate/Download:** Generate and download payslips for all employees.
      * **Time & Attendance Tracking:**
          * **Create:** Manually add/adjust clock-in/out records for employees (with audit trail).
          * **Read:** View all time and attendance data, leave requests, timesheets, attendance calendars.
          * **Update:** Approve/reject leave requests, adjust attendance records.
          * **Delete:** Remove attendance records (with audit trail).
      * **Recruitment & Onboarding:**
          * **Create:** Post new job openings.
          * **Read:** View all job applications, candidate statuses.
          * **Update:** Update candidate status, move through workflows, assign onboarding tasks.
          * **Delete:** Remove job postings or candidate applications.
      * **Performance Management:**
          * **Create:** Set up new performance goals, KPIs.
          * **Read:** View performance reviews, feedback, appraisal data for all employees.
          * **Update:** Update performance reviews, provide feedback.
      * **Learning Management:**
          * **Create:** Assign training programs to employees.
          * **Read:** Track course completion and progress for all employees.
          * **Update:** Update training assignments.
      * **Benefits Administration:**
          * **Create:** Enroll employees in benefit plans.
          * **Read:** View all benefit plan enrollments.
          * **Update:** Modify benefit plan enrollments, approve/reject benefit requests.
      * **Reporting & Analytics:** Generate, download, and export all HR-related reports and access HR dashboard widgets.
      * **Document Management:** Upload and manage employee documents, view all documents.
      * **Compliance Management:** Track labor law compliance, manage policy acceptance.

#### 2.3. Manager Role

The **Manager** role has oversight and approval capabilities for their direct reports.

  * **Access Level:** Limited to direct reports' data and specific management functionalities.
  * **Specific Permissions:**
      * **Employee Information (Direct Reports):**
          * **Read:** View basic information (contact, job role, team) for their direct reports.
          * **Update:** Limited updates (e.g., team assignments, performance notes) for direct reports.
      * **Time & Attendance Tracking (Direct Reports):**
          * **Read:** View time and attendance data, leave requests, timesheets for direct reports.
          * **Update:** Approve/reject leave requests for direct reports.
      * **Performance Management (Direct Reports):**
          * **Create:** Set performance goals for direct reports.
          * **Read:** View performance reviews, feedback, appraisal data for direct reports.
          * **Update:** Conduct performance reviews, provide feedback for direct reports.
      * **Expense Management (Direct Reports):**
          * **Read:** View expense submissions from direct reports.
          * **Update:** Approve/reject expense requests from direct reports.
      * **Manager Self-Service Dashboard:** Access to team dashboards.
      * **Reporting (Limited):** View reports specific to their team's performance, attendance, etc.

#### 2.4. Employee Role

The **Employee** role primarily focuses on self-service functionalities.

  * **Access Level:** Restricted to their own data and common self-service tasks.
  * **Specific Permissions:**
      * **Employee Self-Service:**
          * **Read:** View their own profile information, payslips, leave balances, performance goals.
          * **Update:** Update their own contact information, emergency contacts (profile self-service).
          * **Create:** Submit leave requests, expense claims.
      * **Time & Attendance Tracking:** Clock-in/clock-out, view their own attendance history.
      * **Document Management:** View and download their own documents (e.g., offer letter, payslips).
      * **Learning Management:** View assigned training programs and track their own progress.
      * **Performance Management:** View their own goals, feedback, and performance reviews.

-----

### 3\. Implementing RBAC in FastAPI

Your choice of **JWT-based authentication** and **Role-based access control (RBAC)** in FastAPI is excellent. Here's how you'd typically implement it:

1.  **User Model:** Include a `role` field (e.g., string or enum) in your `User` model.

2.  **Authentication:** After successful JWT authentication, the user's role should be available in the request context.

3.  **Dependency Injection:** Create FastAPI dependencies to check user roles for specific endpoints.

    ```python
    from fastapi import Depends, HTTPException, status
    from app.core.security import get_current_user
    from app.db.models import User

    def role_required(required_roles: list[str]):
        def _role_checker(current_user: User = Depends(get_current_user)):
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
            return current_checker
        return _role_checker

    # Usage in your API routes:
    @router.post("/employees/", dependencies=[Depends(role_required(["admin", "hr"]))])
    async def create_employee(employee: EmployeeCreate):
        # ... logic to create employee
        pass
    ```

-----
### Defined Roles

Based on a typical HRMS and your functional requirements, we can define the following core roles:

1.  **Admin:** Superuser with full control.
2.  **HR:** Manages core HR processes, recruitment, payroll, and employee data.
3.  **Manager:** Oversees their team's performance, attendance, and approvals.
4.  **Employee:** Accesses their own information and self-service features.
5.  **Applicant:** (External Role) For job seekers applying to positions.

---

### Permission Matrix

Here's a detailed matrix outlining the **CRUD (Create, Read, Update, Delete)** operations and specific actions each role can perform across the various modules:

| Module / Feature                | Permission | Admin | HR    | Manager | Employee | Applicant |
| :------------------------------ | :--------- | :---- | :---- | :------ | :------- | :-------- |
| **Employee Information Mgmt.** | Create     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
| **Payroll Management** | Create     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Generate   | ✔     | ✔     | ✗       | ✗        | ✗         |
| **Time & Attendance Tracking** | Create     | ✔     | ✔     | ✗       | Own      | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Approve    | ✔     | ✔     | Team    | ✗        | ✗         |
| **Leave Management** | Create     | ✔     | ✔     | ✗       | Own      | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Approve    | ✔     | ✔     | Team    | ✗        | ✗         |
| **Recruitment & Onboarding** | Create     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Read       | ✔     | ✔     | ✗       | ✗        | Own       |
|                                 | Update     | ✔     | ✔     | ✗       | ✗        | Own       |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Post Job   | ✔     | ✔     | ✗       | ✗        | ✗         |
| **Performance Management** | Create     | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Set Goals  | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Review     | ✔     | ✔     | Team    | Own      | ✗         |
| **Learning Management** | Assign     | ✔     | ✔     | Team    | ✗        | ✗         |
|                                 | Track      | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Complete   | ✗     | ✗     | ✗       | Own      | ✗         |
| **Benefits Administration** | Create     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Read       | ✔     | ✔     | ✗       | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | ✗       | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Enroll     | ✗     | ✗     | ✗       | Own      | ✗         |
|                                 | Approve    | ✔     | ✔     | ✗       | ✗        | ✗         |
| **Reporting & Analytics** | Generate   | ✔     | ✔     | Team    | ✗        | ✗         |
|                                 | View       | ✔     | ✔     | Team    | ✗        | ✗         |
| **Document Management** | Upload     | ✔     | ✔     | ✗       | Own      | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
| **Compliance Management** | Create     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | ✗       | ✗        | ✗         |
| **System Settings** | Manage     | ✔     | ✗     | ✗       | ✗        | ✗         |
| **User & Role Management** | Manage     | ✔     | ✗     | ✗       | ✗        | ✗         |
| **Expense Management** | Create     | ✔     | ✔     | ✗       | Own      | ✗         |
|                                 | Read       | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Update     | ✔     | ✔     | Team    | Own      | ✗         |
|                                 | Delete     | ✔     | ✔     | ✗       | ✗        | ✗         |
|                                 | Approve    | ✔     | ✔     | Team    | ✗        | ✗         |

---

### Key Considerations for RBAC Implementation

* **Granularity:** The matrix provides a good starting point. You might need even finer-grained permissions for specific actions within a module (e.g., "HR can only update certain fields of an employee record").
* **Hierarchical Access:**
    * **Manager Access:** A manager can "Read" and "Update" data for their direct reports/team members, not all employees. This needs to be enforced logically in your backend.
    * **Employee Access:** Employees can only "Read" and "Update" their *own* profile information.
* **Authentication vs. Authorization:**
    * **Authentication (JWT):** Verifies *who* the user is.
    * **Authorization (RBAC):** Determines *what* an authenticated user can do based on their role.
* **API Design:** Your FastAPI endpoints should incorporate decorators or middleware to check the user's role and associated permissions before executing an action.
* **Database Schema:** You'll likely need tables for `Users`, `Roles`, and a many-to-many `user_roles` or a direct `role_id` in the `Users` table for simpler setups.
* **Frontend Impact:** The frontend should dynamically display or hide UI elements (buttons, forms, menu items) based on the logged-in user's role and permissions.
---
### 1. Admin Role

The **Admin** role has **full access** to all modules and functionalities within the HRMS. This includes:

* **Employee Information Management:** CRUD all employee records, including sensitive data.
* **Payroll Management:** CRUD all aspects of payroll setup, processing, and payslip generation.
* **Time & Attendance Tracking:** CRUD all time entries, leave requests, and approval workflows. Override capabilities for attendance.
* **Recruitment & Onboarding:** CRUD all job postings, candidate applications, and onboarding tasks.
* **Performance Management:** CRUD all goals, KPIs, reviews, feedback, and appraisals.
* **Learning Management:** CRUD all training programs, assignments, and track progress.
* **Benefits Administration:** CRUD all benefit plans, enrollments, and approval workflows.
* **Reporting & Analytics:** Access to all reports and dashboards, with full export capabilities.
* **Employee Self-Service:** Can view/manage any employee's self-service data.
* **Manager Self-Service:** Can view/manage any manager's self-service data.
* **Talent Management:** CRUD all career paths and succession plans.
* **Expense Management:** CRUD all expense submissions and approvals.
* **Document Management:** CRUD all employee and system documents, including sensitive legal/HR documents.
* **Compliance Management:** CRUD compliance tracking, policy management, and audit logs.
* **User and Role Management:** CRUD user accounts, assign roles, and manage permissions.
* **System Configuration:** Full access to system-wide settings, integrations, and environment configurations.

---

### 2. HR Role

The **HR** role is a central operational role, focused on managing human resources processes. Their access is broad but typically excludes system-level configurations and some financial overrides.

* **Employee Information Management:**
    * **Create:** Add new employee records.
    * **Read:** View all employee records.
    * **Update:** Modify existing employee records (e.g., job roles, contact info, employment history).
    * **Delete:** Remove employee records (with appropriate audit trails).
* **Payroll Management:**
    * **Create:** Set up new salary structures, pay cycles, and tax/deduction rules.
    * **Read:** View all payroll data, generate and view payslips.
    * **Update:** Modify payroll settings and individual payroll entries.
    * **Delete:** Delete payroll configurations (e.g., a specific deduction rule). *Note: Deleting historical payroll records should be restricted or require special permissions.*
* **Time & Attendance Tracking:**
    * **Create:** Manually add/adjust employee time entries (e.g., for missing clock-ins).
    * **Read:** View all employee attendance, leave requests, and timesheets.
    * **Update:** Approve/reject leave requests, modify attendance records.
    * **Delete:** Delete incorrect time entries or leave requests.
* **Recruitment & Onboarding:**
    * **Create:** Post new job openings, create new candidate profiles.
    * **Read:** View all job applications, candidate statuses, and onboarding task progress.
    * **Update:** Update candidate statuses, assign/complete onboarding tasks.
    * **Delete:** Remove job postings or candidate applications.
* **Performance Management:**
    * **Create:** Set up new performance goals and KPIs for employees, initiate performance reviews.
    * **Read:** View all employee performance data, reviews, and feedback.
    * **Update:** Update performance review statuses, add feedback.
    * **Delete:** Delete performance review drafts (not completed reviews).
* **Learning Management:**
    * **Create:** Assign training programs, create new courses.
    * **Read:** Track course completion and progress for all employees.
    * **Update:** Update training assignments, mark completion.
    * **Delete:** Remove training programs.
* **Benefits Administration:**
    * **Create:** Enroll employees in benefit plans.
    * **Read:** View employee benefit enrollments and plan details.
    * **Update:** Modify benefit enrollments, manage approval workflows.
    * **Delete:** Remove benefit plan enrollments.
* **Reporting & Analytics:**
    * **Read:** Access to all HR-related reports and dashboards.
    * **Export:** Download/export reports (PDF, Excel).
* **Employee Self-Service:**
    * **Read:** Can view/audit employee self-service data.
* **Manager Self-Service:**
    * **Read:** Can view/audit manager self-service data.
* **Talent Management:**
    * **Create:** Set up career paths for employees, initiate succession plans.
    * **Read:** View existing career paths and succession plans.
    * **Update:** Modify career paths and succession planning details.
    * **Delete:** Delete talent management configurations.
* **Expense Management:**
    * **Read:** View all employee expense submissions.
    * **Update:** Approve/reject employee expense claims.
* **Document Management:**
    * **Create:** Upload employee documents.
    * **Read:** View and download employee documents.
    * **Update:** Replace existing documents.
    * **Delete:** Remove employee documents (with audit trail).
* **Compliance Management:**
    * **Create:** Add new compliance policies, track policy acceptance.
    * **Read:** View compliance status, audit logs related to compliance.
    * **Update:** Update compliance policies, track adherence.
    * **Delete:** Remove outdated compliance policies.

---

### 3. Employee Role

The **Employee** role primarily uses the "self-service" functionalities.

* **Employee Information Management:**
    * **Read:** View own employment history, contact information, job role.
    * **Update:** Update own contact information, emergency contacts, and other non-sensitive personal details.
* **Payroll Management:**
    * **Read:** View and download own payslips.
* **Time & Attendance Tracking:**
    * **Create:** Clock-in/clock-out, submit leave requests.
    * **Read:** View own attendance records, leave balances, and leave request status.
    * **Update:** Withdraw or modify pending leave requests.
* **Performance Management:**
    * **Read:** View own goals, KPIs, performance reviews, and feedback.
    * **Update:** Provide self-assessment or feedback during review periods.
* **Learning Management:**
    * **Read:** View assigned training programs, track own course completion.
    * **Update:** Mark courses as completed (if self-paced).
* **Benefits Administration:**
    * **Read:** View own benefit plan enrollments.
    * **Update:** Request changes to benefit enrollments (subject to HR approval).
* **Expense Management:**
    * **Create:** Submit own expense claims.
    * **Read:** Track status of own expense claims.
    * **Update:** Modify pending expense claims.
* **Document Management:**
    * **Read:** View and download own personal documents (e.g., offer letter, policies).
    * **Upload:** Upload personal documents (e.g., expense receipts, certifications).

---

### 4. Manager Role

The **Manager** role has access to information and actions relevant to their direct reports and team.

* **Employee Information Management:**
    * **Read:** View limited employee records for their direct reports (e.g., contact info, job role, department). *No access to sensitive HR data like salary.*
* **Payroll Management:**
    * **Read:** View team's attendance data that impacts payroll. *No access to individual salary details or payslips of direct reports.*
* **Time & Attendance Tracking:**
    * **Read:** View team's attendance records and leave requests.
    * **Update:** Approve/reject leave requests for direct reports.
* **Performance Management:**
    * **Create:** Set goals and KPIs for direct reports, initiate performance reviews for their team.
    * **Read:** View performance data, reviews, and feedback for their direct reports.
    * **Update:** Conduct performance reviews, provide feedback for direct reports.
* **Learning Management:**
    * **Read:** View training progress of direct reports.
    * **Create/Update:** Recommend or assign training programs to direct reports.
* **Expense Management:**
    * **Read:** View expense submissions from direct reports.
    * **Update:** Approve/reject expense claims from direct reports.
* **Reporting & Analytics:**
    * **Read:** Access to team-specific dashboards and reports (e.g., team attendance, leave summaries).
* **Manager Self-Service Dashboard:**
    * **Read:** View key metrics and actions related to their team.

---