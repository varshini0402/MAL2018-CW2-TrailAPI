-- Creating CW2 schema for Assessment 2
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'CW2')
BEGIN
    EXEC('CREATE SCHEMA CW2')
END
GO

-- Dropping existing tables to avoid conflicts
DROP TABLE IF EXISTS CW2.TRAIL_ROUTES;
DROP TABLE IF EXISTS CW2.ROUTE_TYPES;
DROP TABLE IF EXISTS CW2.TRAILS;
GO

-- TRAILS table stores core trail information
CREATE TABLE CW2.TRAILS (
    Trail_ID INT IDENTITY(1,1) PRIMARY KEY,
    Trail_Name VARCHAR(100) NOT NULL,
    Trail_Summary VARCHAR(255),
    Difficulty VARCHAR(20),
    Location VARCHAR(100),
    Length DECIMAL(5,2),
    Elevation_Gain INT,
    Start_Point VARCHAR(150),
    End_Point VARCHAR(150),
    Estimated_Time DECIMAL(4,1),
    Accessibility VARCHAR(255),
    Surface_Type VARCHAR(50),
    Owner_ID INT NOT NULL DEFAULT 1,
    Created_At DATETIME DEFAULT GETDATE(),
    Updated_At DATETIME DEFAULT GETDATE(),
    CONSTRAINT CHK_CW2_Difficulty CHECK (Difficulty IN ('Easy', 'Moderate', 'Hard', 'Expert')),
    CONSTRAINT CHK_CW2_Length CHECK (Length >= 0),
    CONSTRAINT CHK_CW2_Elevation CHECK (Elevation_Gain >= 0)
);
GO

-- ROUTE_TYPES table for categorizing trail types
CREATE TABLE CW2.ROUTE_TYPES (
    Route_Type_ID INT IDENTITY(1,1) PRIMARY KEY,
    Route_Type VARCHAR(50) NOT NULL UNIQUE
);
GO

-- TRAIL_ROUTES links trails with their route types
CREATE TABLE CW2.TRAIL_ROUTES (
    Route_ID INT IDENTITY(1,1) PRIMARY KEY,
    Trail_ID INT NOT NULL,
    Route_Type_ID INT NOT NULL,
    Route_Notes VARCHAR(255),
    CONSTRAINT FK_CW2_TrailRoutes_Trail FOREIGN KEY (Trail_ID) 
        REFERENCES CW2.TRAILS(Trail_ID) ON DELETE CASCADE,
    CONSTRAINT FK_CW2_TrailRoutes_RouteType FOREIGN KEY (Route_Type_ID) 
        REFERENCES CW2.ROUTE_TYPES(Route_Type_ID) ON DELETE CASCADE,
    CONSTRAINT UQ_CW2_Trail_RouteType UNIQUE (Trail_ID, Route_Type_ID)
);
GO

-- Adding route type data
INSERT INTO CW2.ROUTE_TYPES (Route_Type) VALUES
('Loop'),
('Out and Back'),
('Point to Point'),
('Circular');
GO

-- Adding sample trail data for testing
INSERT INTO CW2.TRAILS (
    Trail_Name, Trail_Summary, Difficulty, Location, Length,
    Elevation_Gain, Start_Point, End_Point, Estimated_Time, 
    Accessibility, Surface_Type, Owner_ID
) VALUES
(
    'Plymbridge Circular',
    'A scenic woodland walk through historic Plymbridge Woods',
    'Moderate',
    'Plymouth, Devon',
    6.50,
    120,
    'Plymbridge Woods Car Park',
    'Plymbridge Woods Car Park',
    2.5,
    'Suitable for most fitness levels. Mixed on gravel and woodland trails',
    'Mixed',
    1
),
(
    'Plymouth Waterfront Walk',
    'Coastal walk along Plymouth''s historic waterfront',
    'Easy',
    'Plymouth, Devon',
    4.20,
    50,
    'The Hoe',
    'Sutton Harbour',
    1.5,
    'Wheelchair accessible, paved',
    'Paved',
    1
),
(
    'Dartmoor Ridge Walk',
    'Challenging moorland trek with panoramic views',
    'Hard',
    'Dartmoor, Devon',
    12.00,
    650,
    'Princetown',
    'Postbridge',
    5.0,
    'Experienced hikers only',
    'Rocky moorland',
    1
);
GO

-- Checking if tables were created successfully
SELECT 'CW2 Schema Created Successfully' AS Status;
SELECT COUNT(*) AS Trail_Count FROM CW2.TRAILS;
SELECT COUNT(*) AS RouteType_Count FROM CW2.ROUTE_TYPES;