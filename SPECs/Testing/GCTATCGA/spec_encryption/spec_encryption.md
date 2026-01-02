# Spec: End-to-End Encryption System

**DNA Profile:** GCTATCGA (secure-counselor-notes)  
**Version:** 1.0  
**Date:** 2025-11-02  
**Risk Level:** HIGH

---

## Goal

Implement end-to-end encryption for counselor notes with secure key management, ensuring all patient data is encrypted at rest and in transit with full audit trail.

---

## Components

- Encryption library (libsodium/cryptography.io)
- Key management system
- Secure storage backend
- Audit logging service

---

## Constraints

- Must use AES-256-GCM or stronger
- Keys must never be stored in plaintext
- All encryption events must be logged
- Must comply with HIPAA-like requirements
- Zero-knowledge architecture (server never sees plaintext)

---

## Tasks

### Task 1: Implement Encryption Layer

**TOML Reference:** `tasks[0]`

- **Step 1.1:** Select and configure encryption library
  - **Primary method:** Implement libsodium with sealed boxes for asymmetric encryption
  - **Backup 1:** Use Python cryptography library with Fernet symmetric encryption
  - **Expected output:** Encryption module with encrypt/decrypt functions
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** Test vectors pass, 256-bit key length confirmed
  - **Logging:** Record library choice, algorithm, key length

- **Step 1.2:** Implement key derivation
  - **Primary method:** PBKDF2 with 100,000 iterations from user password
  - **Backup 1:** Argon2id key derivation if PBKDF2 has issues
  - **Expected output:** Key derivation function with salt generation
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** Derived keys are unique per user, computationally expensive
  - **Logging:** Record KDF parameters and performance

- **Step 1.3:** Create encrypted data structure
  - **Primary method:** JSON with encrypted fields: {iv, ciphertext, tag, metadata}
  - **Backup 1:** Use msgpack binary format if JSON has performance issues
  - **Expected output:** Standardised encrypted data format
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** Structure includes all security metadata, validates correctly
  - **Logging:** Record format specification

---

### Task 2: Secure Key Management

**TOML Reference:** `tasks[1]`

- **Step 2.1:** Implement key storage
  - **Primary method:** Store encrypted private keys in database, public keys separately
  - **Backup 1:** Use hardware security module (HSM) emulation if available
  - **Expected output:** Secure key storage with access controls
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** Keys encrypted at rest, access logged, cannot be extracted in plaintext
  - **Logging:** Record storage method and access control tests

- **Step 2.2:** Build key rotation system
  - **Primary method:** Generate new key pair on schedule, re-encrypt data with new key
  - **Backup 1:** Manual key rotation process if automated rotation fails
  - **Expected output:** Automated key rotation every 90 days
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** Old data accessible with old keys, new data uses new keys
  - **Logging:** Record rotation schedule and re-encryption status

- **Step 2.3:** Implement key recovery
  - **Primary method:** Encrypted backup key with multi-factor authentication
  - **Backup 1:** Admin recovery key stored offline with dual-control
  - **Expected output:** Secure key recovery process for lost passwords
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** Recovery requires multiple auth factors, logged extensively
  - **Logging:** Record recovery process and authentication steps

---

### Task 3: Audit Trail System

**TOML Reference:** `tasks[2]`

- **Step 3.1:** Log all encryption events
  - **Primary method:** Write-once audit log with timestamp, user, action, success/failure
  - **Backup 1:** Syslog integration if custom logging fails
  - **Expected output:** Immutable audit log of all cryptographic operations
  - **Critical:** true
  - **Mode:** collaborative
  - **Verification:** All encrypt/decrypt operations logged, tamper-evident
  - **Logging:** Record log storage method and integrity checks

- **Step 3.2:** Implement access monitoring
  - **Primary method:** Real-time alerts on suspicious access patterns
  - **Backup 1:** Batch daily reports if real-time monitoring unavailable
  - **Expected output:** Alert system for unusual encryption activity
  - **Critical:** false
  - **Mode:** silent
  - **Verification:** Alerts trigger on multiple failed decryptions, unusual times
  - **Logging:** Record alert rules and test scenarios

---

## User Stories

- As a counselor, I want my notes encrypted automatically so patient confidentiality is guaranteed
- As a sys admin, I want audit logs of all encryption events so we can prove HIPAA compliance
- As a patient, I want assurance my sensitive information is protected so I can trust the system

---

## Bridging: Markdown ↔ TOML Synchronisation

- Task IDs must match across files
- Step IDs must match
- Critical flags must match (expected: 70% for high-risk)
- Verification steps must align with expected outputs

---

## Instructions for LLM

1. Read DNA profile GCTATCGA: HIGH RISK, collaborative mode, halt_on_critical
2. Verify 70% critical steps (7 of 10 steps marked critical)
3. Pause for human approval at each critical step
4. Halt immediately on any critical failure - do not proceed
5. Log all cryptographic operations with full detail
6. Verify HIPAA-like compliance at each stage
7. User stories inform security-first design decisions



