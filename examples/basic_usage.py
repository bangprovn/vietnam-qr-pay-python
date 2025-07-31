"""Basic usage examples for vietnam-qr-pay."""

from vietnam_qr_pay import QRPay, BanksObject
import qrcode


def print_qr_to_terminal(content, label=""):
    """Print QR code to terminal."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(content)
    qr.make(fit=True)
    
    print(f"\n{label}")
    qr.print_ascii(invert=True)
    print()


def decode_example():
    """Example of decoding a QR code."""
    print("=== Decode VietQR Example ===")
    
    qr_content = "00020101021238530010A0000007270123000697041601092576788590208QRIBFTTA5303704540410005802VN62150811Chuyen tien6304BBB8"
    qr_pay = QRPay(qr_content)
    
    print(f"Valid: {qr_pay.is_valid}")
    print(f"Provider: {qr_pay.provider.name}")
    print(f"Bank BIN: {qr_pay.consumer.bank_bin}")
    print(f"Bank Number: {qr_pay.consumer.bank_number}")
    print(f"Amount: {qr_pay.amount}")
    print(f"Purpose: {qr_pay.additional_data.purpose}")
    
    print_qr_to_terminal(qr_content, "Decoded QR Code:")
    print()


def create_static_vietqr():
    """Example of creating a static VietQR (no amount)."""
    print("=== Create Static VietQR Example ===")
    
    qr_pay = QRPay.init_viet_qr(
        bank_bin=BanksObject["techcombank"].bin,
        bank_number="1457686868"
    )
    
    content = qr_pay.build()
    print(f"QR Content: {content}")
    print_qr_to_terminal(content, "Static VietQR (Techcombank):")
    print()


def create_dynamic_vietqr():
    """Example of creating a dynamic VietQR (with amount)."""
    print("=== Create Dynamic VietQR Example ===")
    
    qr_pay = QRPay.init_viet_qr(
        bank_bin=BanksObject["vietcombank"].bin,
        bank_number="9999999999",
        amount="100000",
        purpose="Thanh toan don hang #123"
    )
    
    content = qr_pay.build()
    print(f"QR Content: {content}")
    print(f"Bank: {BanksObject['vietcombank'].short_name}")
    print(f"Amount: {qr_pay.amount} VND")
    print_qr_to_terminal(content, "Dynamic VietQR (Vietcombank with 100,000 VND):")
    print()


def create_vnpay_qr():
    """Example of creating a VNPay QR."""
    print("=== Create VNPay QR Example ===")
    
    qr_pay = QRPay.init_vnpay_qr(
        merchant_id="0102154778",
        merchant_name="CONG TY ABC",
        store="CHI NHANH 1",
        terminal="POS001",
        amount="250000",
        purpose="Thanh toan hoa don"
    )
    
    content = qr_pay.build()
    print(f"QR Content: {content}")
    print_qr_to_terminal(content, "VNPay QR (250,000 VND):")
    print()


def list_supported_banks():
    """Example of listing all supported banks."""
    print("=== Supported Banks ===")
    
    transfer_banks = [
        bank for bank in BanksObject.values() 
        if bank.viet_qr_status == 1
    ]
    
    print(f"Total banks supporting transfer: {len(transfer_banks)}")
    print("\nSome popular banks:")
    
    popular_banks = ["vietcombank", "acb", "techcombank", "mbbank", "vpbank"]
    for bank_key in popular_banks:
        bank = BanksObject[bank_key]
        print(f"- {bank.short_name}: BIN {bank.bin}")
    print()


if __name__ == "__main__":
    decode_example()
    create_static_vietqr()
    create_dynamic_vietqr()
    create_vnpay_qr()
    list_supported_banks()