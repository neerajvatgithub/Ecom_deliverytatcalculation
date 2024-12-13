# Delivery TAT Calculator

A Streamlit application to calculate and analyze delivery Turn Around Time (TAT) for e-commerce orders.

## Features

- Calculate time differences between:
  - Order Creation to Approval
  - Order Creation to Delivery
  - Approval to Delivery
- Display summary statistics (Average, Minimum, Maximum)
- Show detailed time differences in days, hours, and minutes
- Download processed data as CSV

## Requirements

- Python 3.8+
- Streamlit
- Pandas

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ecom_deliveryTAT.git
cd ecom_deliveryTAT
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run main.py
```

2. Upload your CSV file with the following columns:
   - created_on
   - approval date and time
   - Delivery date and time
   - order_id
   - shipping_address_city

3. View the calculated TAT metrics and download processed data

## Input Data Format

The CSV file should contain dates in the format:
- Example: "Friday, November 15, 2024, 9:21:12 PM"

## License

MIT License 