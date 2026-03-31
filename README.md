# unknownapp
This is an unknown application written in Java

---- For Submission (you must fill in the information below) ----
### Use Case Diagram

![E2E6890C-D4A2-4316-9284-76B67807EE5A](https://github.com/user-attachments/assets/f168c195-3336-448a-9888-7ea56c72050f)

### Flowchart of the main workflow

```mermaid
flowchart TD
    START([Start]) --> INIT["Load data / seed default"]
    INIT --> LOGIN

    LOGIN[/"Login Menu"/]
    LOGIN --> D_LOGIN{Choose option?}
    D_LOGIN -->|Student| SLOGIN["Enter Student ID"]
    D_LOGIN -->|Admin| ALOGIN["Enter Password"]
    D_LOGIN -->|Exit| SAVE_EXIT["Save & exit"]
    SAVE_EXIT --> END([End])

    %% ── Student path ──────────────────────────────
    SLOGIN --> D_ID{"ID = 'new'?"}
    D_ID -->|Yes| CREATE["Create new profile"]
    D_ID -->|No| D_FOUND{"ID found\nin system?"}
    D_FOUND -->|Not found| SLOGIN
    D_FOUND -->|Found| SMENU

    CREATE --> D_VALID{"Is data\nvalid?"}
    D_VALID -->|No| SLOGIN
    D_VALID -->|Yes| SMENU

    SMENU[/"Student Menu"/]
    SMENU --> D_SMENU{Choose action?}
    D_SMENU --> S1["View catalog"]
    D_SMENU --> S2["Register course"]
    D_SMENU --> S3["Drop course"]
    D_SMENU --> S4["View schedule"]
    D_SMENU --> S5["Billing summary"]
    D_SMENU --> S6["Edit profile"]
    D_SMENU -->|Logout| SAVE_S["Save data"]

    S2 --> D_ENROLL{"Can enroll?"}
    D_ENROLL -->|Success| SMENU
    D_ENROLL -->|Failed| SMENU

    S1 & S3 & S4 & S5 & S6 --> SMENU
    SAVE_S --> LOGIN

    %% ── Admin path ─────────────────────────────────
    ALOGIN --> D_PWD{"Password\ncorrect?"}
    D_PWD -->|No| LOGIN
    D_PWD -->|Yes| AMENU

    AMENU[/"Admin Menu"/]
    AMENU --> D_AMENU{Choose action?}
    D_AMENU --> A1["View catalog / roster"]
    D_AMENU --> A2["View all students"]
    D_AMENU --> A3["Add / edit student"]
    D_AMENU --> A4["Add / edit course"]
    D_AMENU --> A5["View student schedule"]
    D_AMENU --> A6["Billing summary"]
    D_AMENU -->|Logout| SAVE_A["Save data"]

    A3 --> D_STUD{"Duplicate / existing ID?"}
    D_STUD -->|No duplicate| AMENU
    D_STUD -->|Duplicate / not found| AMENU

    A4 --> D_COURSE{"Duplicate / existing course code?"}
    D_COURSE -->|No duplicate| AMENU
    D_COURSE -->|Duplicate / not found| AMENU

    A1 & A2 & A5 & A6 --> AMENU
    SAVE_A --> LOGIN

    %% ── Styles ──────────────────────────────────────
    classDef teal   fill:#1D9E75,stroke:#0F6E56,color:#fff
    classDef coral  fill:#D85A30,stroke:#993C1D,color:#fff
    classDef amber  fill:#BA7517,stroke:#854F0B,color:#fff
    classDef gray   fill:#888780,stroke:#5F5E5A,color:#fff
    classDef decide fill:#7F77DD,stroke:#534AB7,color:#fff

    class SLOGIN,CREATE,SMENU,S1,S2,S3,S4,S5,S6,SAVE_S teal
    class ALOGIN,AMENU,A1,A2,A3,A4,A5,A6,SAVE_A coral
    class LOGIN,INIT,SAVE_EXIT amber
    class START,END gray
    class D_LOGIN,D_ID,D_FOUND,D_VALID,D_SMENU,D_ENROLL,D_PWD,D_AMENU,D_STUD,D_COURSE decide
```

### Prompts

create an equivalent Python version of the program for the loginMenu, studentLogin, and createStudentProfile, adminLogin studentMenu, adminMenu sections. Put the Python program in a new folder called “python.” 
