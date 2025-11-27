# https://theworld.com/~reinhold/diceware.txt

import time
import sqlite3
import secrets
import click
import json
from tqdm import tqdm
from rich import print as rprint
from rich.panel import Panel
from rich.console import Console
from rich.text import Text

# Initialize Rich console for styled output
console = Console()


def get_word_by_number(number:int) -> str:
    """
    Retrieve a word from the diceware database based on a 5-digit dice number.
    
    Args:
        number (int): 5-digit number representing dice rolls (11111-66666)
        
    Returns:
        str: The corresponding word from the diceware list, or False if not found
    """

    try:
        conn = sqlite3.connect('diceware.db')
        cursor = conn.cursor()
        cursor.execute('SELECT word FROM diceware WHERE number = ?', (number,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            # Log the missing number for debugging
            console.log(f"Warning: Number {number} not found in database")
            return None
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def number_generator() -> int:
    """
    Generate a random 5-digit number simulating 5 dice rolls (1-6 each).
    
    Returns:
        int: 5-digit number representing dice rolls
    """
    secure_random = secrets.SystemRandom()
    
    base_numbers = ''.join(str(secure_random.randint(1, 6)) for _ in range(5))
    number = int(base_numbers)

    if number > 65433:
        number_generator()
    
    return number


def password_number_generator(count:int) -> int:
    """
    Generate a random number of specified digit count.
    
    Args:
        count (int): Number of digits to generate
        
    Returns:
        int: Random number with specified digit count
    """
    base_numbers = str()
    secure_random = secrets.SystemRandom()
    for i in range(count):
        number = secure_random.randint(0, 9)
        base_numbers += str(number)

    return int(base_numbers)
    

def special_characters() -> str:
    """
    Select a random special character from a predefined list.
    
    Returns:
        str: Random special character
    """
    specs = ["!", "!!", "\"", "#", "##", "$", "$$", "%", "%%", "&", "(", "()", ")", "*", "**", "+", "-", ":", ";", "=", "?", "??", "@"]
    base_numbers = str()
    secure_random = secrets.SystemRandom()
    
    number = secure_random.randint(0, len(specs) - 1)
    base_numbers += specs[number]

    return base_numbers


def genarate_words(number_of_dice_rolls:int=4) -> list:
    """
    Generate a list of random words using the diceware method.
    
    Args:
        number_of_dice_rolls (int): Number of words to generate (default: 4)
        
    Returns:
        list: List of randomly selected words
    """
    words:list = list()
    for i in range(number_of_dice_rolls):
        num = number_generator()
        word = get_word_by_number(num)
        if word:
            words.append(word)

    return words


def generate_password(number_of_dice_rolls:int=4, nums:int=0, char:int=0, caps:int=0) -> str:
    """
    Generate a complete password/passphrase with optional enhancements.
    
    Args:
        number_of_dice_rolls (int): Number of words in passphrase
        nums (int): Number of random digits to append
        char (int): Number of special characters to append  
        caps (bool): Whether to capitalize words
        
    Returns:
        tuple: (list of words/components, final password string)
    """

    # Input validation
    if number_of_dice_rolls < 2:
        raise ValueError("Number of dice rolls must be at least 2")
    if nums < 0 or char < 0:
        raise ValueError("Number of digits and characters cannot be negative")

    # Generate base words using diceware method
    words = genarate_words(number_of_dice_rolls)

    # Ensure we have exactly the requested number of words
    max_retries = 10
    retries = 0
    while len(words) != number_of_dice_rolls and retries < max_retries:
        words = genarate_words(number_of_dice_rolls)
        retries += 1

    if len(words) != number_of_dice_rolls:
        raise RuntimeError(f"Failed to generate {number_of_dice_rolls} words after {max_retries} retries")
    

    # Capitalize first letter of each word if requested
    if caps == True:
        for i in range(len(words)):
            words[i] = words[i][0].upper() + words[i][1:]

    # Add random numbers if requested
    if nums > 0:
        numbers = password_number_generator(nums)
        words.append(str(numbers))

    # Add special characters if requested
    if char > 0:
        specs:list = list()
        for i in range(char):
            specs.append(special_characters())
        words += specs

     # Combine all components into final password string
    final = ''.join(words)

    return (words, final)


@click.command()
@click.option('--dice-rolls', type=int, default=4, help='number of dice rolls')
@click.option('--nums', type=click.IntRange(0, 10), default=0, 
              help='Number of random digits to add (0-10)')
@click.option('--char', type=click.IntRange(0, 10), default=0, 
              help='Number of special characters to add (0-10)')
@click.option('--caps/--no-caps', default=False, 
              help='Capitalize first letter of each word')
def main(dice_rolls, nums, char, caps):
    """Generate high-entropy passwords the easy way!"""
    console.clear()

    # Display welcome panel with Rich styling
    rprint(Panel('Generate high-entropy passwords the easy way!', title="Diceware Password Generator"))

    # Generate the password/passphrase
    items, finals = generate_password(dice_rolls, nums, char, caps)
    total_items = len(items)            

    # Display progress bar while "generating" words
    with tqdm(total=total_items, desc="Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as progress:
        for item in items:
            progress.set_description(f"Item: {item}")
            time.sleep(0.5)
            progress.update(1)
    
    time.sleep(1)

    # Estimate password strength based on number of items
    if total_items == 2:
        pos = "60 million"
    elif total_items == 3:
        pos = "470 billion"
    elif total_items == 4:
        pos = "3 quadrillion"
    elif total_items == 5:
        pos = "28 quintillion"
    elif total_items == 6:
        pos = "221 sextillion"
    elif total_items == 7:
        pos = "1 octillion"
    elif total_items == 8:
        pos = "13 nonillion"


    # Create word list display
    word_display = "\n".join([f"{i+1}. {word}" for i, word in enumerate(items)])

    # Strength analysis

    content = f"""
[bold]Your words:[/bold]
{word_display}

[bold]Your passphrase:[/bold]
[green]{finals}[/green]
"""
    console.print(Panel(content, title="Diceware Password", subtitle=f"of possible passwords: {pos}", border_style="green"))

if __name__ == '__main__':
    main()