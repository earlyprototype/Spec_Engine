-- CreateTable
CREATE TABLE "dna_profiles" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "dnaCode" TEXT NOT NULL,
    "projectName" TEXT NOT NULL,
    "testing" TEXT NOT NULL,
    "risk" TEXT NOT NULL,
    "autonomy" TEXT NOT NULL,
    "customTools" TEXT,
    "constraints" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "specs" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "descriptor" TEXT NOT NULL,
    "dnaCode" TEXT NOT NULL,
    "goal" TEXT NOT NULL DEFAULT '',
    "status" TEXT NOT NULL DEFAULT 'pending',
    "filePath" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "specs_dnaCode_fkey" FOREIGN KEY ("dnaCode") REFERENCES "dna_profiles" ("dnaCode") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "executions" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "specId" TEXT NOT NULL,
    "mode" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "goalStatus" TEXT,
    "startedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" DATETIME,
    "duration" INTEGER,
    "errorMessage" TEXT,
    CONSTRAINT "executions_specId_fkey" FOREIGN KEY ("specId") REFERENCES "specs" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "progress_logs" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "executionId" TEXT NOT NULL,
    "taskId" TEXT,
    "stepId" TEXT,
    "status" TEXT NOT NULL,
    "method" TEXT,
    "timestamp" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "details" TEXT,
    CONSTRAINT "progress_logs_executionId_fkey" FOREIGN KEY ("executionId") REFERENCES "executions" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "dna_profiles_dnaCode_key" ON "dna_profiles"("dnaCode");

-- CreateIndex
CREATE INDEX "specs_dnaCode_idx" ON "specs"("dnaCode");

-- CreateIndex
CREATE INDEX "specs_status_idx" ON "specs"("status");

-- CreateIndex
CREATE UNIQUE INDEX "specs_dnaCode_descriptor_key" ON "specs"("dnaCode", "descriptor");

-- CreateIndex
CREATE INDEX "executions_specId_idx" ON "executions"("specId");

-- CreateIndex
CREATE INDEX "executions_status_idx" ON "executions"("status");

-- CreateIndex
CREATE INDEX "progress_logs_executionId_idx" ON "progress_logs"("executionId");

-- CreateIndex
CREATE INDEX "progress_logs_timestamp_idx" ON "progress_logs"("timestamp");
