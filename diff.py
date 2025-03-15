def parse_file(filename):
    """Parse a file into followers and following sets."""
    with open(filename, 'r', encoding='utf-8-sig') as f:  # Changed here
        lines = [line.strip() for line in f.readlines()]
    
    followers = set()
    following = set()
    current_section = None
    
    for line in lines:
        if not line:
            continue
        if line == "Followers:":
            current_section = "followers"
        elif line == "Following:":
            current_section = "following"
        else:
            if ':' in line:
                username = line
                if current_section == "followers":
                    followers.add(username)
                elif current_section == "following":
                    following.add(username)
    
    return followers, following

def print_changes(title, added, removed):
    """Print changes in a formatted way."""
    print(f"\n{title}")
    print("-" * 50)
    
    if added:
        print("\nNewly Added:")
        for user in sorted(added):
            print(f"+ {user}")
    
    if removed:
        print("\nRecently Removed:")
        for user in sorted(removed):
            print(f"- {user}")
    
    if not added and not removed:
        print("No changes")

def main(old_file, new_file):
    # Parse both files
    old_followers, old_following = parse_file(old_file)
    new_followers, new_following = parse_file(new_file)
    
    # Calculate differences
    followers_added = new_followers - old_followers
    followers_removed = old_followers - new_followers
    
    following_added = new_following - old_following
    following_removed = old_following - new_following
    
    # Print results
    print("=" * 50)
    print("FOLLOWERS CHANGES")
    print(f"Number of old Followers: {len(old_followers)} \nNumber of new Followers {len(new_followers)}")
    print_changes("Followers Changes:", followers_added, followers_removed)
    
    print("\n" + "=" * 50)
    print("FOLLOWING CHANGES")
    print(f"Number of old Followers: {len(old_following)} \nNumber of new Followers {len(new_following)}")
    print_changes("Following Changes:", following_added, following_removed)
    print("=" * 50)

def mainStart(oldFile, newFile):
    import sys
    
    if not oldFile or not newFile:
        print("Usage: enter oldfile and newfile path")
        sys.exit(1)
    
    main(oldFile,newFile)