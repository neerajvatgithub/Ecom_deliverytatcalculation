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
git clone https://github.com/neerajvatgithub/Ecom_deliverytatcalculation.git
cd Ecom_deliverytatcalculation
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
   - Created time
   - Approval time
   - Delivered time
   - order_id

3. View the calculated TAT metrics and download processed data

## Input Data Format

The CSV file should contain dates in any of the following formats:
- `Monday, April 21, 2025, 11:45:14 PM`
- `Monday, April 21, 2025 at 11:45:14 PM`
- `Monday, April 21, 2025, 11:45 PM`
- `Monday, April 21, 2025 at 11:45 PM`
- `12/12/24 23:33`
- `12/13/2024 10:25`
- `12/13/2024 10:25:00`

**Example CSV:**
| order_id | Created time                        | Approval time                        | Delivered time                       |
|----------|-------------------------------------|--------------------------------------|--------------------------------------|
| OID41591 | Monday, April 21, 2025 at 11:45:14 PM | Tuesday, April 22, 2025 at 8:36:52 AM | Tuesday, April 22, 2025 at 10:09:55 AM |

## License

MIT License 