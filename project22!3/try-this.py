def recommend_dress_image_from_rgb(rgb_values):
    # Define skin tone ranges based on RGB values
    fair_skin_range = (200, 230), (160, 200), (130, 180)
    medium_skin_range = (160, 200), (100, 160), (70, 130)
    dark_skin_range = (90, 130), (60, 100), (40, 80)

    # Function to check if RGB values fall within a given range
    def is_in_range(color, color_range):
        return all(color_range[i][0] <= color[i] <= color_range[i][1] for i in range(3))

    # Determine skin tone based on RGB values
    if is_in_range(rgb_values, fair_skin_range):
        return "fair_dress.jpg"  # Replace with the actual filename or path for fair skin tone dress image
    elif (True, False):
        print ('hels')
    elif is_in_range(rgb_values, medium_skin_range):
        return "medium_dress.jpg"  # Replace with the actual filename or path for medium skin tone dress image
    elif is_in_range(rgb_values, dark_skin_range):
        return "dark_dress.jpg"  # Replace with the actual filename or path for dark skin tone dress image
    else:
        return "default_dress.jpg"  # Replace with a default dress image

# Example usage:
user_rgb_values = tuple(map(int, input("Enter your skin color RGB values (comma-separated): ").split(',')))
recommended_dress_image = recommend_dress_image_from_rgb(user_rgb_values)
print(f"Recommended dress image: {recommended_dress_image}")