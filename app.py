def get_user_profile(user_id):
    raw_phone = "0987654321"
    raw_email = "student@ptit.edu.vn"
    masked_phone = raw_phone[:3] + "****" + raw_phone[-3:]
    masked_email = raw_email[:2] + "****@" + raw_email.split("@")[1]
    return {
        "user_id": user_id,
        "phone": masked_phone,
        "email": masked_email,
        "version": "1.0.1"
    }

if __name__ == "__main__":
    profile = get_user_profile(101)
    print(profile)
