// Get gender selection from the user
// Retrieve selected gender from sessionStorage
const selectedGender = sessionStorage.getItem('selectedGender');
const selectedOccsion = sessionStorage.getItem('selectedOccasion');
console.log("Selected gender:", selectedGender);
console.log("Selected Occasion:", selectedOccsion);

// Function to recommend dress image based on RGB values
function recommendDressImageFromRGB(rgbValues) {
    // Define skin tone ranges based on RGB values
    const fairSkinRange = [[235, 255], [190, 225], [160, 190]]; // Fair
    const lightSkinRange = [[220, 245], [170, 205], [140, 170]]; // Light
    const mediumSkinRange = [[195, 220], [145, 180], [120, 160]]; // Medium
    const oliveSkinRange = [[170, 195], [120, 155], [90, 130]]; // Olive
    const tanSkinRange = [[145, 170], [100, 135], [70, 100]]; // Tan
    const brownSkinRange = [[120, 145], [80, 110], [50, 90]]; // Brown
    const deepSkinRange = [[70, 120], [40, 90], [20, 60]]; // Deep

    // Convert RGB Arrays to Array
    // const rgbValue =s rgbValues

    // Function to check if RGB values fall within a given range
    // Function to check if RGB values fall within a given range
    function isInRange(color, colorRange) {
        // Count the number of channels that fall within the range
        const channelsInRange = color.reduce((count, val, i) => {
            if (val >= colorRange[i][0] && val <= colorRange[i][1]) {
                return count + 1;
            }
            return count;
        }, 0);

        // If at least two channels are within the range, return true
        return channelsInRange >= 2;
    }


    // Determine skin tone based on RGB values
    if (isInRange(rgbValues, fairSkinRange)) {
        return "fair_skin";  // Replace with the actual skin tone identifier
    } else if (isInRange(rgbValues, lightSkinRange)) {
        return "light_skin";  // Replace with the actual skin tone identifier
    } else if (isInRange(rgbValues, mediumSkinRange)) {
        return "medium_skin";  // Replace with the actual skin tone identifier
    } else if (isInRange(rgbValues, oliveSkinRange)) {
        return "olive_skin";  // Replace with the actual skin tone identifier
    } else if (isInRange(rgbValues, tanSkinRange)) {
        return "tan_skin";  // Replace with the actual skin tone identifier
    } else if (isInRange(rgbValues, brownSkinRange)) {
        return "brown_skin";  // Replace with the actual skin tone identifier
    } else if (isInRange(rgbValues, deepSkinRange)) {
        return "deep_skin";  // Replace with the actual skin tone identifier
    } else {
        return null;  // No matching skin tone found
    }
}

// Fetch dress images based on skin tone and gender from external JSON file
// Fetch dress images based on skin tone, gender, and occasion
async function fetchDressImagesWithDescriptions(skinTone, gender, occasion) {
    try {
        const response = await fetch('static/dress_images.json');
        const data = await response.json();
        console.log(occasion)
        console.log(data[skinTone]);
        console.log(data[skinTone][gender]);
        console.log(data[skinTone][gender][occasion]);
        return data[skinTone][gender][occasion];
    } catch (error) {
        console.error('Error fetching dress images:', error);
        return [];
    }
}

// Function to get the highest RGB channel values from an array of colors
function getHighestRGB(rgbValues) {
    // Initialize variables to store the highest RGB values
    let highestRed = 0;
    let highestGreen = 0;
    let highestBlue = 0;

    // Loop through each color array and update the highest RGB values
    rgbValues.forEach(color => {
        const [red, green, blue] = color;
        highestRed = Math.max(highestRed, red);
        highestGreen = Math.max(highestGreen, green);
        highestBlue = Math.max(highestBlue, blue);
    });

    // Return an array containing the highest RGB values
    return [highestRed, highestGreen, highestBlue];
}

// Get RGB values from dominant color info
const rgbValues = dominantColorsData.map(color => color.color);
console.log(rgbValues);

// Get the highest RGB channel values
const highestRGBValues = getHighestRGB(rgbValues);
console.log(highestRGBValues);

// Recommend dress image based on RGB values
const recommendedSkinTone = recommendDressImageFromRGB(highestRGBValues);
console.log(recommendedSkinTone)
if (recommendedSkinTone) {
    // Fetch dress images based on the recommended skin tone, gender, and occasion
    fetchDressImagesWithDescriptions(recommendedSkinTone, selectedGender, selectedOccsion)
        .then(imagesWithDescriptions => {
            console.log("from create ele",imagesWithDescriptions)
            // Get the advised dress container
            const advisedDressContainer = document.querySelector('.advised-dress div:last-child');

            // Loop through each dress image and description
            imagesWithDescriptions.forEach(item => {
                // Create a <div> container for the image and description
                const divElement = document.createElement('div');
                divElement.classList.add('advised-image');

                // Create an <img> element for the dress image
                const imgElement = document.createElement('img');
                imgElement.src = item.image;
                imgElement.alt = 'Advised Dress';

                // Create a <p> element for the description
                const pElement = document.createElement('p');
                pElement.textContent = item.description;

                // Append the <img> and <p> elements to the <div> container
                divElement.appendChild(imgElement);
                divElement.appendChild(pElement);

                // Append the <div> container to the advised dress container
                advisedDressContainer.appendChild(divElement);
            });
        })
        .catch(error => {
            console.error('Error fetching dress images:', error);
            // Display an error message to the user
            const errorMessage = document.createElement('p');
            errorMessage.textContent = 'An error occurred while fetching dress images. Please try again later.';
            // Append the error message to the advised dress container
            advisedDressContainer.appendChild(errorMessage);
        });
} else {
    console.log('No matching skin tone found.');
    // Display a fallback message to the user
    const fallbackMessage = document.createElement('p');
    fallbackMessage.textContent = 'We couldn\'t find a matching skin tone for your selection. Please try again with different options.';
    // Append the fallback message to the advised dress container
    advisedDressContainer.appendChild(fallbackMessage);
}

