# Bynry
# 📦 StockFlow – B2B Inventory Management System

Welcome to **StockFlow**, a B2B inventory management platform designed for small businesses to efficiently track products across multiple warehouses, manage supplier relationships, and monitor inventory levels.

This repository includes the backend implementation for the StockFlow platform, covering the following tasks:

---

## ✅ Project Overview

### Part 1 – Code Review & Debugging
- Reviewed and fixed an API endpoint for adding new products.
- Handled issues such as SKU uniqueness, multi-warehouse support, and optional fields.
- Implemented validations and error handling for better reliability.

### Part 2 – Database Design
- Designed a normalized database schema using SQLAlchemy.
- Created tables for products, warehouses, suppliers, sales, inventory, and thresholds.
- Documented missing requirements and justified design decisions (indexes, constraints, etc.).

### Part 3 – API Implementation
- Built a Flask endpoint that returns low-stock alerts for a company.
- Handled business rules such as:
  - Thresholds based on product types.
  - Alerts only for products with recent sales activity.
  - Multiple warehouses per company.
  - Inclusion of supplier information for reordering.
- Provided fallback mechanisms and handled edge cases gracefully.

---

## 📂 Project Structure

