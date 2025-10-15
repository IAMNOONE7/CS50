-- Keep a log of any SQL queries you execute as you solve the mystery.
.headers on
.mode column
-- =================================================================================
-- What exactly happend
--SELECT *
--FROM crime_scene_reports
--WHERE year = 2024 AND month = 7 AND DAY = 28
--AND street = 'Humphrey Street';

-- =================================================================================
-- Get witnesses interviews
--SELECT name, transcript
--FROM interviews
--WHERE year = 2024 AND month = 7 AND day = 28
--AND transcript LIKE '%bakery%';

-- =================================================================================
-- We need to find one person who satisfies all clues

--SELECT *
--FROM bakery_security_logs
--WHERE year = 2024 AND month = 7 AND day = 28
--AND hour = 10 AND minute BETWEEN 15 AND 25
--AND activity = 'exit'

--SELECT p.id, p.name, p.phone_number, p.license_plate
--FROM atm_transactions at
--JOIN bank_accounts ba ON ba.account_number = at.account_number
--JOIN people p ON p.id = ba.person_id
--WHERE at.year = 2024 AND at.month = 7 AND at.day = 28
--AND at.atm_location LIKE 'Legget%'

--SELECT DISTINCT p.id, p.name, p.phone_number, pc.receiver, pc.duration
--FROM phone_calls pc
--JOIN people p ON pc.caller = p.phone_number
--WHERE pc.year = 2024 AND pc.month = 7 AND pc.day = 28
--AND pc.duration < 60;

-- join
/*
WITH bakery_plates AS (
    SELECT DISTINCT license_plate
    FROM bakery_security_logs
    WHERE year = 2024 AND month = 7 AND day = 28
    AND hour = 10 AND minute BETWEEN 15 AND 25
    AND activity = 'exit'
),

ATM AS (
    SELECT DISTINCT ba.person_id
    FROM atm_transactions at
    JOIN bank_accounts ba ON ba.account_number = at.account_number
    JOIN people p ON p.id = ba.person_id
    WHERE at.year = 2024 AND at.month = 7 AND at.day = 28
    AND at.atm_location LIKE 'Legget%'
),
short_calls AS(
    SELECT DISTINCT p.id AS person_id, pc.receiver
    FROM phone_calls pc
    JOIN people p ON pc.caller = p.phone_number
    WHERE pc.year = 2024 AND pc.month = 7 AND pc.day = 28
    AND pc.duration < 60
)

SELECT p.id, p.name AS thief, p.phone_number, p.license_plate, sc.receiver AS accomplie_phone
FROM people p
JOIN short_calls sc ON sc.person_id = p.id
WHERE p.id IN (SELECT person_id FROM ATM)
AND p.license_plate IN (SELECT license_plate FROM bakery_plates)*/

-- =================================================================================
-- who actually left the city
--SELECT id, full_name
--FROM airports
--WHERE city LIKE '%Fiftyville%';
-- ID is 8

/*SELECT id AS flight_id, destination_airport_id, hour, minute
FROM flights
WHERE origin_airport_id = 8
AND year = 2024 AND month = 7 AND day = 29
ORDER by hour, minute
LIMIT 1*/
-- destination = 4

/*SELECT id, full_name, city
FROM airports
WHERE id = 4;*/
-- NEW YORK
/*
SELECT p.name, p.phone_number, p.passport_number
FROM passengers pa
JOIN people p ON pa.passport_number = p.passport_number
WHERE pa.flight_id = 36*/
/*
SELECT name
FROM people
WHERE phone_number IN('(725) 555-3243','(375) 555-8161')

*/
-- =================================================================================
-- Seems like it is Bruce and Robin






