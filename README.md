# Diceware Password Generator

A secure and user-friendly password/passphrase generator based on the Diceware method for creating high-entropy passwords that are both strong and memorable.

## Features

- **Diceware Method**: Generates passwords using the proven Diceware wordlist method
- **Cryptographically Secure**: Uses Python's `secrets` module for true randomness
- **Customizable Output**: Add numbers, special characters, and capitalization
- **Rich Visual Interface**: Beautiful terminal output with progress bars and formatted panels
- **Strength Estimation**: Provides entropy estimates for generated passwords
- **SQLite Backend**: Fast word lookup from local database

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure you have the `diceware.db` SQLite database file in the same directory

## Usage

### Basic Usage

Generate a simple 4-word passphrase (default):

```bash
python main.py
```

### Advanced Options

```bash
python main.py --dice-rolls 5 --nums 2 --char 1 --caps
```

**Command Line Options:**

- `--dice-rolls`: Number of words in passphrase (default: 4, min: 2)
- `--nums`: Number of random digits to append (0-10)
- `--char`: Number of special characters to append (0-10)  
- `--caps/--no-caps`: Capitalize first letter of each word (default: False)

### Examples

**Simple memorable passphrase:**
```bash
python main.py --dice-rolls 4

╭─────────────────────────────────────── Diceware Password Generator ────────────────────────────────────────╮
│ Generate high-entropy passwords the easy way!                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Item: rk: 100%|██████████████████████████████████████████████████████████████████████████████████████████| 4/4
╭──────────────────────────────────────────── Diceware Password ─────────────────────────────────────────────╮
│                                                                                                            │
│ Your words:                                                                                                │
│ 1. poke                                                                                                    │
│ 2. torso                                                                                                   │
│ 3. rude                                                                                                    │
│ 4. rk                                                                                                      │
│                                                                                                            │
│ Your passphrase:                                                                                           │
│ poketorsoruderk                                                                                            │
│                                                                                                            │
╰─────────────────────────────────── of possible passwords: 3 quadrillion ───────────────────────────────────╯
     
```

**Strong password with enhancements:**
```bash
python main.py --dice-rolls 5 --nums 3 --char 2 --caps

╭─────────────────────────────────────── Diceware Password Generator ────────────────────────────────────────╮
│ Generate high-entropy passwords the easy way!                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
Item: =: 100%|███████████████████████████████████████████████████████████████████████████████████████████| 8/8
╭──────────────────────────────────────────── Diceware Password ─────────────────────────────────────────────╮
│                                                                                                            │
│ Your words:                                                                                                │
│ 1. Padre                                                                                                   │
│ 2. Creak                                                                                                   │
│ 3. Sex                                                                                                     │
│ 4. Lisp                                                                                                    │
│ 5. Gyp                                                                                                     │
│ 6. 448                                                                                                     │
│ 7. ?                                                                                                       │
│ 8. =                                                                                                       │
│                                                                                                            │
│ Your passphrase:                                                                                           │
│ PadreCreakSexLispGyp448?=                                                                                  │
│                                                                                                            │
╰─────────────────────────────────── of possible passwords: 13 nonillion ────────────────────────────────────╯
               

```

## Security Features

- **True Randomness**: Uses `secrets.SystemRandom()` for cryptographically secure random number generation
- **Diceware Method**: Each word provides ~12.9 bits of entropy
- **Local Database**: No network calls required during generation
- **Input Validation**: Prevents invalid parameter combinations

## Password Strength

The generator provides entropy estimates based on the number of words:

- 2 words: ~60 million possible combinations
- 3 words: ~470 billion possible combinations  
- 4 words: ~3 quadrillion possible combinations
- 5 words: ~28 quintillion possible combinations
- 6 words: ~221 sextillion possible combinations

## How It Works

1. Generates random 5-digit numbers (11111-66666) simulating dice rolls
2. Looks up corresponding words from the Diceware wordlist database
3. Optionally adds numbers, special characters, and capitalization
4. Combines all elements into a final password string

## Requirements

- Python 3.6+
- click
- tqdm  
- rich
- sqlite3 (standard library)

## License

This tool is based on the Diceware method created by Arnold G. Reinhold. The Diceware wordlist is in the public domain.

## Security Notes

- Generated passwords are displayed only in the terminal and not stored
- For maximum security, use at least 6 words for important accounts
- Consider using a password manager to store generated passwords securely
- The strength estimates are approximations - actual security depends on implementation and usage

## Contributing

Feel free to submit issues and enhancement requests!