function getBotResponse(input) {
    
    if (input == "hello") {
        return "Hello there! How are you feeling today?";
    } else if (input == "goodbye") {
        return "Talk to you later!";
    } else if (input == "How are you?") {
        return "I'm good";
    } else if (input == "bye") {
        return "Talk to you later!";
    } else if (input == "I'm good") {
        return "That is great!";
    } else {
        return "I dont understand, ask me something else!";
    }
}