import pyodbc

class dbManager:

    def __init__(self):
        with open("app.config", "r") as file:
            self.connectionString = file.read()

    def getTodayComments(self):
        query = self.generateBasicQuery()
        
        conn = pyodbc.connect(self.connectionString)
        with conn:
            cursor = conn.cursor().execute(query)
            cursor.execute(query)
            return cursor.fetchall()

    def getPageOfComments(self, skip, take):
        query = self.generatePaginatedQuery(skip, take)
        
        conn = pyodbc.connect(self.connectionString)
        with conn:
            cursor = conn.cursor().execute(query)
            cursor.execute(query)
            return cursor.fetchall()

    def generateBasicQuery(self):
        query = """
        SELECT DISTINCT TOP 500 [Text] as [text] 
	    ,[Tickets].[FriendlyId] as [id]
        FROM [SupportCenterPaid].[c1f0951c-3885-44cf-accb-1a390f34c342].[Posts]
        INNER JOIN [SupportCenterPaid].[c1f0951c-3885-44cf-accb-1a390f34c342].[Tickets] 
	        on [Tickets].[Id] = [Posts].[Ticket_Id] 
        INNER JOIN [SupportCenterPaid].[c1f0951c-3885-44cf-accb-1a390f34c342].[Users] 
	        on [Users].[Id] = [Posts].[Owner]

        WHERE
		[Posts].[Modified] > CAST(CURRENT_TIMESTAMP AS DATE)
		and
		[Users].[IsEmployee] = 0
        """
        return query

    def generatePaginatedQuery(self, skip, take):
        query = """
        SELECT [Text] as [text] 
	    ,[Tickets].[FriendlyId] as [id]
        FROM [SupportCenterPaid].[c1f0951c-3885-44cf-accb-1a390f34c342].[Posts]
        INNER JOIN [SupportCenterPaid].[c1f0951c-3885-44cf-accb-1a390f34c342].[Tickets] 
	        on [Tickets].[Id] = [Posts].[Ticket_Id] 
        INNER JOIN [SupportCenterPaid].[c1f0951c-3885-44cf-accb-1a390f34c342].[Users] 
	        on [Users].[Id] = [Posts].[Owner]

        WHERE
		[Users].[IsEmployee] = 0

        ORDER BY [Posts].[Modified] DESC 
        OFFSET %d ROWS
        FETCH NEXT %d ROWS ONLY
        """ % (skip, take)
        return query
