# ✅ HR Data Pipeline – Validation Report

This document tracks data quality checks after loading `company_db` into MySQL.

_Last updated: {{YYYY-MM-DD}}_

---

## 🔍 Table Summary

| Table             | Expected Rows | Actual Rows | Pass/Fail |
|------------------|---------------|-------------|-----------|
| departments       | 8             | ✅           | ✅        |
| employees         | 1,000         | ✅           | ✅        |
| projects          | 25,000        | ✅           | ✅        |
| employee_project  | ~5,000+       | ✅           | ✅        |
| attendance        | ~2M+          | ✅           | ✅        |
| bonuses           | ≥500          | ✅           | ✅        |
| payroll           | 12,000        | ✅           | ✅        |
| leaves            | ≥2,000        | ✅           | ✅        |
| training          | ≥1,000        | ✅           | ✅        |
| assets            | ≥1,000        | ✅           | ✅        |

---

## 📊 Validation Checks

### ✔️ 1. Foreign Keys

- [x] All `employees.department_id` match `departments.department_id`
- [x] All `employee_project.empID` exist in `employees`
- [x] All `attendance.empID` exist in `employees`

### ✔️ 2. Nulls in Critical Fields

- [x] No NULL `employee_name` values
- [x] No NULL `project_name` values
- [x] All `payroll.net_salary` values present

### ✔️ 3. Date Ranges

- [x] `date_of_birth` < `join_date` for all employees
- [x] `attendance.date` spans 2020–2025
- [x] No future dates in `payroll`, `bonuses`, `leaves`, etc.

### ✔️ 4. Value Sanity

| Field         | Rule                       | Status |
|---------------|----------------------------|--------|
| salary        | Between ₹70K–₹290K         | ✅     |
| bonus_amount  | Between ₹0–₹100K           | ✅     |
| leave_status  | Only: Approved/Pending/Rejected | ✅ |

---

## 📄 Notes / Observations

- All tables successfully exported and formatted.
- Log file saved at `dump/process.log`
- No schema mismatch or integrity violation found.

---

✅ *Project validation completed. Dataset ready for analytics, dashboards, and demo deployment.*

