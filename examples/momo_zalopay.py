"""Examples for creating MoMo and ZaloPay QR codes."""

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


def create_momo_qr():
    """Create a MoMo QR code example."""
    print("=== MoMo QR Example ===")
    
    # MoMo account number from the app
    account_number = "99MM24011M34875080"
    
    # Create QR using Bản Việt bank (MoMo's partner bank)
    momo_qr = QRPay.init_viet_qr(
        bank_bin=BanksObject["banviet"].bin,
        bank_number=account_number,
        amount="50000",  # Optional
        purpose="Chuyen tien cho MoMo"  # Optional
    )
    
    # Add MoMo specific reference
    momo_qr.additional_data.reference = "MOMOW2W" + account_number[10:]
    
    # Add phone number's last 3 digits (example: 046)
    momo_qr.set_unreserved_field("80", "046")
    
    content = momo_qr.build()
    print(f"QR Content: {content}")
    print(f"Account: {account_number}")
    print(f"Reference: {momo_qr.additional_data.reference}")
    print_qr_to_terminal(content, "MoMo QR Code:")
    print()


def create_zalopay_qr():
    """Create a ZaloPay QR code example."""
    print("=== ZaloPay QR Example ===")
    
    # ZaloPay account number from the app
    account_number = "99ZP24009M07248267"
    
    # Create QR using Bản Việt bank (ZaloPay's partner bank)
    zalopay_qr = QRPay.init_viet_qr(
        bank_bin=BanksObject["banviet"].bin,
        bank_number=account_number,
        amount="100000",  # Optional
        purpose="Thanh toan ZaloPay"  # Optional
    )
    
    content = zalopay_qr.build()
    print(f"QR Content: {content}")
    print(f"Account: {account_number}")
    print_qr_to_terminal(content, "ZaloPay QR Code:")
    print()


def decode_momo_qr():
    """Decode an existing MoMo QR code."""
    print("=== Decode MoMo QR Example ===")
    
    # Example MoMo QR content
    qr_content = "00020101021138620010A00000072701320006970454011899MM24011M348750800208QRIBFTTA53037045802VN62190515MOMOW2W3487508080030466304EBC8"
    
    qr_pay = QRPay(qr_content)
    
    if qr_pay.is_valid:
        print(f"Bank: {qr_pay.consumer.bank_bin}")
        print(f"Account: {qr_pay.consumer.bank_number}")
        print(f"Reference: {qr_pay.additional_data.reference}")
        print(f"Phone suffix: {qr_pay.unreserved.get('80', 'N/A')}")
        print_qr_to_terminal(qr_content, "Decoded MoMo QR:")
    else:
        print("Invalid QR code")
    print()


if __name__ == "__main__":
    create_momo_qr()
    create_zalopay_qr()
    decode_momo_qr()