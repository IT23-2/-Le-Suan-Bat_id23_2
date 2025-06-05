import subprocess


def extract_encrypted_data(archive_path, output_file='encrypted_data.txt'):
    try:
        command_result = subprocess.run(['john-bleeding-jumbo/run/rar2john', archive_path], capture_output=True,
                                        text=True)

        if command_result.returncode != 0 or not command_result.stdout:
            print("rar2john завершился с ошибкой:")
            print(command_result.stderr)
            return False

        with open(output_file, 'w') as data_file:
            data_file.write(command_result.stdout)

        print(f"Данные успешно извлечены и сохранены в {output_file}")
        return True

    except FileNotFoundError:
        print("rar2john не найден. Убедитесь, что вы указали правильный путь: ./run/rar2john")
        return False


encrypted_archive = 'john-bleeding-jumbo/f.rar'
extract_encrypted_data(encrypted_archive)


def decrypt_password():
    with open('encrypted_data.txt', 'r') as data_file:
        hash_value = data_file.read().split(':', 1)[1]

    dictionary_file = 'wordlist.txt'

    with open('rar5_hash.txt', 'w') as hash_file:
        hash_file.write(hash_value)

    subprocess.run([
        'hashcat',
        '-m', '13000',
        '-a', '0',
        'rar5_hash.txt',
        dictionary_file,
        '--force'
    ])

    result = subprocess.check_output([
        'hashcat',
        '-m', '13000',
        'rar5_hash.txt',
        '--show'
    ]).decode()

    if ':' in result:
        password = result.strip().split(':', 1)[1]
        with open('recovered_password.txt', 'w') as password_file:
            password_file.write(password + '\n')
        print(f'[+] Пароль найден и сохранен в recovered_password.txt: {password}')
    else:
        print('[-] Пароль не найден.')


decrypt_password()
