# unknownapp
This is an unknown application written in Java

---- For Submission (you must fill in the information below) ----
### Use Case Diagram

%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#e1f5fe', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff'}}}%%
usecaseDiagram
    actor Student as "Student\n(นักศึกษา)"
    actor Admin as "Admin\n(ผู้ดูแลระบบ)"

    package "Course Enrollment System" {
        usecase UC1 as "Login / Create Profile\n(เข้าสู่ระบบ/สร้างโปรไฟล์)"
        usecase UC2 as "View Course Catalog\n(ดูรายชื่อวิชา)"
        usecase UC3 as "Register for a Course\n(ลงทะเบียนเรียน)"
        usecase UC4 as "Drop a Course\n(ยกเลิกรายวิชา)"
        usecase UC5 as "View My Schedule\n(ดูตารางเรียนตนเอง)"
        usecase UC6 as "View Billing Summary\n(ดูสรุปค่าใช้จ่าย)"
        usecase UC7 as "Edit My Profile\n(แก้ไขข้อมูลส่วนตัว)"
        
        usecase UC8 as "Admin Login\n(เข้าสู่ระบบ Admin)"
        usecase UC9 as "Manage Students\n(จัดการข้อมูลนักศึกษา)"
        usecase UC10 as "Manage Courses\n(จัดการข้อมูลวิชา)"
        usecase UC11 as "View Class Roster\n(ดูรายชื่อนักศึกษาในวิชา)"
        usecase UC12 as "Monitor Student Activity\n(ดูตารางเรียน/ค่าใช้จ่ายนักศึกษาทุกคน)"
        
        usecase UC13 as "Save Data\n(บันทึกข้อมูลอัตโนมัติ)"
    }

    %% Student Relationships
    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Student --> UC5
    Student --> UC6
    Student --> UC7

    %% Admin Relationships
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12

    %% System Relationships (Hidden)
    UC1 ..> UC13 : <<include>>
    UC3 ..> UC13 : <<include>>
    UC4 ..> UC13 : <<include>>
    UC7 ..> UC13 : <<include>>
    UC8 ..> UC13 : <<include>>
    UC9 ..> UC13 : <<include>>
    UC10 ..> UC13 : <<include>>
    
### Flowchart of the main workflow

### Prompts
