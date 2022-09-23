# Government Grant Distribution

An amazing & educational API that simulates the relationship between
a family household needs and grant eligibility.

## Tech Stack

**Server:** Flask, mySQL

## Environment Variables

To run this project, you will need to update the following environment variables to your .env file at root directory.

`DB_ACCOUNT_ID` : -mySQL username-

`DB_ACCOUNT_PASSWORD` : -mySQL password-

## Requirements

**mySQL Database**

Navigate to `./App` directory and copy the contents in `schema.sql`.
Execute the SQL script in a mySQL server (WAMP,MAMP,XAMPP,etc) of your choice to initiate the database tables and mock values.

**Chances if env variables cannot be detected, might be buggy.**

Please navigate to `./App/settings.py`, edit `SQLALCHEMY_DATABASE_URI` variable to config for the DB database connection.
Replace `{os.environ.get("DB_ACCOUNT_ID")}` with DB account ID and `{os.environ.get("DB_ACCOUNT_PASSWORD")}` with DB password. <blank if needed>
Change hostname and DB port number if required.

## Run Locally

#### Clone the project

```bash
git clone https://github.com/JarBarKar/government-grant-disbursement.git
```

#### Go to the project directory

```bash
cd government-grant-disbursement
```

#### Create virtual environment

-Mac-

```bash
python3 -m venv venv
```

-Windows-

```bash
py -3 -m venv venv
```

#### Activate virtual environment

-Mac-

```bash
. venv/bin/activate
```

-Windows-

```bash
venv\Scripts\activate
```

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Start the Flask server

```bash
flask --app App --debug run
```

## API Reference

#### List all households

```bash
  GET /household/all
```

#### Search for a specific household

```bash
  GET /household/search?id=<household_id>
```

| Parameter      | Type     | Description                            |
| :------------- | :------- | :------------------------------------- |
| `household_id` | `string` | **Required**. Id of household to fetch |

#### Create a household

```bash
  POST /household/add
```

| Parameter        | Type  | Description                     | Options (seperated by ,) |
| :--------------- | :---- | :------------------------------ | :----------------------- |
| `household_type` | `int` | **Required**. Type of household | Landed,Condominium,HDB   |

#### Add a family member to household

```bash
  POST /household/add_member
```

| Parameter         | Type      | Description                                       | Options (seperated by ,)                               |
| :---------------- | :-------- | :------------------------------------------------ | :----------------------------------------------------- |
| `household_id`    | `int`     | **Required**. Household id                        | Landed,Condominium,HDB                                 |
| `name`            | `string`  | **Required**. Name of family member               | -                                                      |
| `gender`          | `string`  | **Required**. Member's gender                     | male,female,m,f                                        |
| `marital_status`  | `string`  | **Required**. Member's marital status             | single,married,widowed,seperated,divorced,not reported |
| `spouse`          | `string`  | Name of spouse                                    | -                                                      |
| `occupation_type` | `string`  | **Required**. Type of occupation                  | unemployed,student,employed                            |
| `annual_income`   | `decimal` | **Required**. Member's income per year            | -                                                      |
| `dob`             | `date`    | **Required**. Member's date of birth <dd/mm/YYYY> |                                                        |

#### List the households and qualifying family members of grant disbursement

```bash
  GET /household/grant_schemes?grant=<name_of_grant>
```

| Parameter       | Type     | Description                     | Options (seperated by ,)                                                                          |
| :-------------- | :------- | :------------------------------ | :------------------------------------------------------------------------------------------------ |
| `name_of_grant` | `string` | **Required**. Name of the grant | student-encouragement-bonus,multigeneration-scheme,elder-bonus,baby-sunshine-grant,yolo-gst-grant |

#### Type of grant

| Parameter                | Name of grant               | Criteria                                                                                                                        | Members eligible             |
| :----------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------ | :--------------------------- |
| `student-encouragement`  | Student Encouragement Bonus | Households with member(s) that is/are a student of less than 16 years old **&** Households income of less than $200,000.        | Members < 16 years old       |
| `multigeneration-scheme` | Multigeneration Scheme      | Households with either member(s) <18 years or member(s) above the age of 55 **&** Households with income of less than $150,000. | All members of the household |
| `elder-bonus`            | Elder Bonus                 | HDB households with members above the age of 55                                                                                 | Member(s) >= 55 years old    |
| `baby-sunshine-grant`    | Baby Sunshine Grant         | Households with member(s) younger than 8 months old                                                                             | Member(s) < 8 months old     |
| `yolo-gst-grant`         | YOLO GST Grant              | HDB households with annual income of less than $100,000.                                                                        | All members of the household |

## Postman Collection

You can import the postman collections in the root directory to call the API endpoints.

## FAQ

#### Why no unit test, docker, deployment?!

I want to focus on my time in enhancing and improving the core requirements first.
And I am not comfortable in rushing out additional features given the limited time...

#### Can I contribute to this project?

Yes, anyone can! :D

## Authors

- [@JarBarKar](https://www.github.com/JarBarKar)
