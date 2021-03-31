# Entity Relationship Diagrams

## MVP

```mermaid
erDiagram

    %%
    %% Entities
    %%

    SIC_Code {
      string title
      int code
    }

    User {
      string email
    }

    Company {
      string name
      string number
      employees number
      address address
      m2m jurisdictions
      m2m sic_codes
    }

    Regulator {
      string name
      string url
      m2m sic_codes
    }

    Jurisdiction {
      string name
      string slug
    }

    Region {
      string name
      string slug
      fk jurisdiction
    }

    Category {
      string name
      string slug
    }

    %% Jurisdiction could be removed and inferred from regions
    Regulation {
      string name
      string description
      string url
      boolean is_blanket
      enum importance
      m2m regulators
      m2m jurisdictions
      m2m regions
      m2m sic_codes
      m2m categories
    }

    Guidance {
      string title
      url url
      fk regulation
    }

    Tracker {
      fk user
      fk company
      m2m regulations
    }

    Subscription {
      email email
      string mobile_number
      enum frequency
      datetime last_update
      jsonfield filters
      fk user
    }

    %%
    %% Relationships
    %%

    %% Company
    Company ||--|| User : has
    Company }|--|{ SIC_Code : includes
    Company ||--|{ Jurisdiction : has

    %% Regulations
    Regulation }|--|{ Regulator : includes
    Regulation }|--|{ Jurisdiction : includes
    Regulation }|--|{ Region : includes
    Jurisdiction ||--|{ Region : has
    Regulation }|--|{ SIC_Code : includes
    Regulation }|--|{ Category : includes
    Regulation }|--|| Guidance : has
    Regulator }|--|{ SIC_Code : includes

    %% Tracker
    Tracker ||--|| Company : has
    Tracker }|--|{ Regulation : includes

    %% Notifications
    Subscription ||--o| User : subscribes
    Subscription }|--|{ Regulation : "regulation updates trigger notifications"
```

## Future

```mermaid
erDiagram

    %%
    %% Entities
    %%

    SIC_Code {
      string title
      int code
    }

    User {
      string email
    }

    Company {
      string name
      string number
      employees number
      address address
      m2m jurisdictions
      m2m sic_codes
    }

    Regulator {
      string name
      string url
      m2m sic_codes
    }

    Jurisdiction {
      string name
      string slug
    }

    Region {
      string name
      string slug
      fk jurisdiction
    }

    Category {
      string name
      string slug
    }

    %% Jurisdiction could be removed and inferred from regions
    Regulation {
      string name
      string description
      string url
      boolean is_blanket
      enum importance
      m2m regulators
      m2m jurisdictions
      m2m regions
      m2m sic_codes
      m2m categories
    }

    Guidance {
      string title
      url url
      fk regulation
    }

    Tracker {
      fk user
      fk company
      m2m regulations
    }

    Activity {
      int id
      int activity_code
      string title
      text description
      fk sic_code
    }

    Subscription {
      email email
      string mobile_number
      enum frequency
      datetime last_update
      jsonfield filters
      fk user
    }

    %%
    %% Relationships
    %%

    %% Company
    Company ||--|{ User : "has one or more"
    Company }|--|{ SIC_Code : includes
    Company ||--|{ Jurisdiction : has

    %% Regulations
    Regulation }|--|{ Regulator : includes
    Regulation }|--|{ Jurisdiction : includes
    Regulation }|--|{ Region : includes
    Jurisdiction ||--|{ Region : has
    Regulation }|--|{ SIC_Code : includes
    Regulation }|--|{ Category : includes
    Regulation }|--|| Guidance : has
    Regulator }|--|{ SIC_Code : includes

    %% Tracker
    Tracker ||--|| Company : has
    Tracker }|--|{ Regulation : includes

    %% Activity
    Activity ||--|| SIC_Code : "belongs to"
    Company ||--o{ Activity : has
    Regulation ||--o{ Activity : "relevant for"
    Guidance ||--o{ Activity : "relevant for"

    %% Notifications
    Subscription ||--o| User : subscribes
    Subscription }|--|{ Regulation : "regulation updates trigger notifications"
```
