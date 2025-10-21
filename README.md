# PDF Invoice Stamping Automation

## 📋 Description

**PDF Invoice Stamping Automation** is a Python-based tool that automatically adds digital stamps and company signatures to PDF invoices. This application streamlines the document approval process by batch-processing multiple PDF files with customizable stamps and dynamic text.

### 🌟 Key Features

- **🔄 Batch Processing**: Automatically processes all PDF files in a designated folder
- **🏷️ Custom Stamping**: Adds both image stamps and dynamic text to PDF documents
- **⚙️ Configurable Settings**: Adjustable stamp position, size, and text content
- **🔍 Smart File Detection**: Automatically detects PDF files with case-insensitive search
- **📁 Organized Workflow**: Separate input/output folders for better file management
- **🐛 Error Handling**: Comprehensive error reporting and folder diagnostics

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Required Python packages:
  ```bash
  pip install PyPDF2 reportlab
  ```

### Installation

1. **Clone or download the project files**
2. **Set up the folder structure** (automatically created on first run):
   ```
   project-folder/
   ├── invoices/                 # Place input PDF files here
   ├── signed_invoices/          # Stamped PDFs will be saved here
   └── stamp-blue.png           # Your stamp image file
   ```

3. **Configure the settings** in the `main()` function:
   ```python
   SETTINGS = {
       'input_directory': 'path/to/your/invoices',
       'output_directory': 'path/to/your/signed_invoices',
       'stamp_image_path': 'path/to/your/stamp-image.png',
       'company_name': 'Your Company Name',
       'position_settings': {
           'stamp_x': 400,        # Horizontal position
           'stamp_y': 50,         # Vertical position  
           'stamp_width': 150,    # Stamp width
           'stamp_height': 100,   # Stamp height
           'text_y_offset': -20   # Text position adjustment
       }
   }
   ```

4. **Run the application**:
   ```bash
   python pdf_stamper.py
   ```

## 📖 Usage

### Basic Operation

1. Place your PDF invoice files in the `invoices` folder
2. Ensure your stamp image file is in the specified location
3. Run the script
4. Find processed files in the `signed_invoices` folder with `_signed.pdf` suffix

### Customization Options

- **Stamp Position**: Adjust `stamp_x` and `stamp_y` coordinates
- **Stamp Size**: Modify `stamp_width` and `stamp_height`
- **Company Text**: Change `company_name` for dynamic text display
- **Text Positioning**: Use `text_y_offset` to position text relative to stamp

## 🛠️ Technical Details

### Core Functions

- `create_stamp_pdf()`: Generates temporary PDF with stamp image and text
- `apply_stamp_to_pdf()`: Merges stamp PDF with original invoice
- `get_invoice_files()`: Smart PDF file detection with error handling
- `process_invoice_pdfs()`: Main processing function with batch operations

### Supported Formats

- **Input**: PDF files (.pdf)
- **Stamps**: PNG, JPG, JPEG, BMP, GIF images
- **Output**: PDF files with embedded stamps

## 📝 Code Example

```python
# Process invoices with custom settings
processed_files = process_invoice_pdfs(
    input_directory='./invoices',
    output_directory='./signed_invoices', 
    stamp_image_path='./stamp.png',
    company_name='My Business LLC',
    position_settings={
        'stamp_x': 400,
        'stamp_y': 50,
        'stamp_width': 150,
        'stamp_height': 100,
        'text_y_offset': -20
    }
)
```

## 🐛 Troubleshooting

### Common Issues

1. **No PDF files found**
   - Verify files have `.pdf` extension
   - Check input directory path
   - Ensure files are not corrupted

2. **Stamp image not found**
   - Verify image file exists in specified location
   - Check file permissions
   - Ensure supported image format

3. **Positioning problems**
   - Adjust coordinates based on your PDF layout
   - Test with different `stamp_x` and `stamp_y` values
   - Consider PDF page size variations

### Diagnostic Features

- Automatic folder content display
- Detailed error messages
- File count and processing status
- Success/failure reporting

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](#) if you want to contribute.

## 📞 Support

If you encounter any problems or have questions, please open an issue in the project repository.

---

**⭐ If you find this project useful, please give it a star!**
