import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  SafeAreaView,
  ActivityIndicator,
} from "react-native";

const API_URL = "http://localhost:5000";

export default function HomeScreen() {
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(false);

  const [weather, setWeather] = useState({
    city: "New Delhi",
    temperature: 28,
    condition: "Partly Cloudy",
    humidity: 72,
    wind: 14,
    feelsLike: 30,
    icon: "☁️",
  });

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hi! I'm WeatherGPT. Ask me anything about the weather, forecast, alerts or climate.",
    },
  ]);

  const searchWeather = async () => {
    if (!city.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/api/weather?city=${encodeURIComponent(city)}`
      );

      if (!response.ok) {
        throw new Error("Weather API error");
      }

      const data = await response.json();

      setWeather({
        city: data.city || city,
        temperature: data.temperature || 28,
        condition: data.condition || "Partly Cloudy",
        humidity: data.humidity || 72,
        wind: data.wind_speed || 14,
        feelsLike: data.feels_like || 30,
        icon: data.icon || "☁️",
      });
    } catch (error) {
      setWeather({
        city: city,
        temperature: 28,
        condition: "Partly Cloudy",
        humidity: 72,
        wind: 14,
        feelsLike: 30,
        icon: "☁️",
      });
    }

    setLoading(false);
  };

  const askWeatherGPT = async () => {
    if (!question.trim()) {
      return;
    }

    const userQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      {
        sender: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userQuestion,
          city: weather.city,
        }),
      });

      if (!response.ok) {
        throw new Error("Chat API error");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          sender: "ai",
          text:
            data.response ||
            data.message ||
            "I couldn't generate a response.",
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          sender: "ai",
          text: `I'm ready to answer questions about ${weather.city}. The AI backend will be connected next.`,
        },
      ]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >

        {/* HEADER */}

        <View style={styles.header}>
          <View>
            <Text style={styles.logo}>WeatherGPT</Text>

            <Text style={styles.subtitle}>
              Your AI-powered weather assistant
            </Text>
          </View>

          <View style={styles.aiCircle}>
            <Text style={styles.aiText}>AI</Text>
          </View>
        </View>

        {/* SEARCH */}

        <View style={styles.searchBox}>
          <Text style={styles.searchIcon}>⌖</Text>

          <TextInput
            style={styles.searchInput}
            placeholder="Enter your city"
            placeholderTextColor="#8194B0"
            value={city}
            onChangeText={setCity}
            onSubmitEditing={searchWeather}
          />

          <TouchableOpacity
            style={styles.searchButton}
            onPress={searchWeather}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.searchButtonText}>
                Search
              </Text>
            )}
          </TouchableOpacity>
        </View>

        {/* CURRENT WEATHER */}

        <View style={styles.weatherCard}>
          <View>
            <Text style={styles.cardLabel}>
              CURRENT WEATHER
            </Text>

            <Text style={styles.city}>
              {weather.city}
            </Text>

            <Text style={styles.temperature}>
              {weather.temperature}°
            </Text>

            <Text style={styles.condition}>
              {weather.condition}
            </Text>
          </View>

          <Text style={styles.weatherIcon}>
            {weather.icon}
          </Text>
        </View>

        {/* WEATHER DETAILS */}

        <View style={styles.detailsRow}>

          <DetailCard
            icon="💧"
            value={`${weather.humidity}%`}
            label="Humidity"
          />

          <DetailCard
            icon="💨"
            value={`${weather.wind} km/h`}
            label="Wind"
          />

          <DetailCard
            icon="🌡️"
            value={`${weather.feelsLike}°`}
            label="Feels like"
          />

        </View>

        {/* FORECAST */}

        <Text style={styles.sectionTitle}>
          5-Day Forecast
        </Text>

        <View style={styles.forecastCard}>

          <Forecast
            day="Today"
            icon="☁️"
            temp="28°"
          />

          <Forecast
            day="Sat"
            icon="🌤️"
            temp="30°"
          />

          <Forecast
            day="Sun"
            icon="☀️"
            temp="31°"
          />

          <Forecast
            day="Mon"
            icon="🌧️"
            temp="27°"
          />

          <Forecast
            day="Tue"
            icon="⛅"
            temp="29°"
          />

        </View>

        {/* AI CHAT */}

        <Text style={styles.sectionTitle}>
          Ask WeatherGPT
        </Text>

        <View style={styles.chatCard}>

          {messages.map((message, index) => (

            <View
              key={index}
              style={
                message.sender === "user"
                  ? styles.userMessage
                  : styles.aiMessage
              }
            >

              {message.sender === "ai" && (
                <View style={styles.smallAI}>
                  <Text style={styles.smallAIText}>
                    AI
                  </Text>
                </View>
              )}

              <View
                style={
                  message.sender === "user"
                    ? styles.userBubble
                    : styles.aiBubble
                }
              >

                <Text style={styles.messageText}>
                  {message.text}
                </Text>

              </View>

            </View>

          ))}

          <View style={styles.chatInputBox}>

            <TextInput
              style={styles.chatInput}
              placeholder="Ask about the weather..."
              placeholderTextColor="#8194B0"
              value={question}
              onChangeText={setQuestion}
              onSubmitEditing={askWeatherGPT}
            />

            <TouchableOpacity
              style={styles.sendButton}
              onPress={askWeatherGPT}
            >

              <Text style={styles.sendText}>
                ➤
              </Text>

            </TouchableOpacity>

          </View>

        </View>

        {/* ALERTS */}

        <Text style={styles.sectionTitle}>
          Weather Alerts
        </Text>

        <View style={styles.alertCard}>

          <Text style={styles.alertIcon}>
            ⚠️
          </Text>

          <View style={styles.alertContent}>

            <Text style={styles.alertTitle}>
              No active alerts
            </Text>

            <Text style={styles.alertText}>
              We'll notify you when severe weather
              conditions are detected.
            </Text>

          </View>

        </View>

        {/* CLIMATE */}

        <Text style={styles.sectionTitle}>
          Climate Information
        </Text>

        <View style={styles.climateCard}>

          <Text style={styles.climateTitle}>
            🌍 Understanding your climate
          </Text>

          <Text style={styles.climateText}>
            Get insights about temperature trends,
            rainfall patterns, climate change and
            long-term weather conditions.
          </Text>

          <TouchableOpacity>
            <Text style={styles.exploreText}>
              Explore Climate Data →
            </Text>
          </TouchableOpacity>

        </View>

        <Text style={styles.footer}>
          WeatherGPT • AI-powered weather intelligence
        </Text>

      </ScrollView>
    </SafeAreaView>
  );
}


// WEATHER DETAIL CARD

function DetailCard({
  icon,
  value,
  label,
}: {
  icon: string;
  value: string;
  label: string;
}) {
  return (
    <View style={styles.detailCard}>

      <Text style={styles.detailIcon}>
        {icon}
      </Text>

      <Text style={styles.detailValue}>
        {value}
      </Text>

      <Text style={styles.detailLabel}>
        {label}
      </Text>

    </View>
  );
}


// FORECAST CARD

function Forecast({
  day,
  icon,
  temp,
}: {
  day: string;
  icon: string;
  temp: string;
}) {
  return (
    <View style={styles.forecastDay}>

      <Text style={styles.forecastDayText}>
        {day}
      </Text>

      <Text style={styles.forecastIcon}>
        {icon}
      </Text>

      <Text style={styles.forecastTemp}>
        {temp}
      </Text>

    </View>
  );
}


// STYLES

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: "#071A33",
  },

  content: {
    padding: 20,
    paddingBottom: 50,
  },

  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 25,
  },

  logo: {
    fontSize: 30,
    fontWeight: "800",
    color: "#FFFFFF",
  },

  subtitle: {
    color: "#91A4C4",
    fontSize: 13,
    marginTop: 4,
  },

  aiCircle: {
    width: 46,
    height: 46,
    borderRadius: 23,
    backgroundColor: "#16365F",
    justifyContent: "center",
    alignItems: "center",
  },

  aiText: {
    color: "#65C7FF",
    fontWeight: "800",
  },

  searchBox: {
    height: 55,
    backgroundColor: "#102846",
    borderRadius: 15,
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    marginBottom: 20,
  },

  searchIcon: {
    fontSize: 22,
    color: "#65C7FF",
    marginRight: 8,
  },

  searchInput: {
    flex: 1,
    color: "#FFFFFF",
    fontSize: 15,
  },

  searchButton: {
    backgroundColor: "#2997FF",
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 10,
    minWidth: 72,
    alignItems: "center",
  },

  searchButtonText: {
    color: "#FFFFFF",
    fontWeight: "700",
  },

  weatherCard: {
    backgroundColor: "#12345A",
    borderRadius: 22,
    padding: 24,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 15,
  },

  cardLabel: {
    color: "#72C9FF",
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 1,
  },

  city: {
    color: "#FFFFFF",
    fontSize: 22,
    fontWeight: "700",
    marginTop: 7,
  },

  temperature: {
    color: "#FFFFFF",
    fontSize: 58,
    fontWeight: "300",
    marginTop: 5,
  },

  condition: {
    color: "#B7C7DD",
    fontSize: 15,
  },

  weatherIcon: {
    fontSize: 70,
  },

  detailsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 25,
  },

  detailCard: {
    backgroundColor: "#102846",
    width: "31.5%",
    paddingVertical: 15,
    borderRadius: 15,
    alignItems: "center",
  },

  detailIcon: {
    fontSize: 20,
  },

  detailValue: {
    color: "#FFFFFF",
    fontWeight: "700",
    marginTop: 5,
  },

  detailLabel: {
    color: "#8194B0",
    fontSize: 11,
    marginTop: 3,
  },

  sectionTitle: {
    color: "#FFFFFF",
    fontSize: 20,
    fontWeight: "700",
    marginBottom: 12,
    marginTop: 8,
  },

  forecastCard: {
    backgroundColor: "#102846",
    borderRadius: 18,
    padding: 15,
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 25,
  },

  forecastDay: {
    alignItems: "center",
  },

  forecastDayText: {
    color: "#91A4C4",
    fontSize: 12,
  },

  forecastIcon: {
    fontSize: 24,
    marginVertical: 8,
  },

  forecastTemp: {
    color: "#FFFFFF",
    fontWeight: "700",
  },

  chatCard: {
    backgroundColor: "#102846",
    borderRadius: 18,
    padding: 15,
    marginBottom: 25,
  },

  aiMessage: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 12,
  },

  userMessage: {
    flexDirection: "row",
    justifyContent: "flex-end",
    marginBottom: 12,
  },

  smallAI: {
    width: 35,
    height: 35,
    borderRadius: 18,
    backgroundColor: "#2997FF",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 10,
  },

  smallAIText: {
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "800",
  },

  aiBubble: {
    backgroundColor: "#173A62",
    borderRadius: 14,
    padding: 12,
    maxWidth: "82%",
  },

  userBubble: {
    backgroundColor: "#2997FF",
    borderRadius: 14,
    padding: 12,
    maxWidth: "82%",
  },

  messageText: {
    color: "#FFFFFF",
    lineHeight: 20,
    fontSize: 14,
  },

  chatInputBox: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#071A33",
    borderRadius: 12,
    paddingLeft: 12,
    marginTop: 8,
  },

  chatInput: {
    flex: 1,
    color: "#FFFFFF",
    height: 45,
  },

  sendButton: {
    width: 45,
    height: 45,
    backgroundColor: "#2997FF",
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },

  sendText: {
    color: "#FFFFFF",
    fontSize: 20,
  },

  alertCard: {
    backgroundColor: "#102846",
    borderRadius: 18,
    padding: 18,
    flexDirection: "row",
    marginBottom: 25,
  },

  alertIcon: {
    fontSize: 25,
    marginRight: 12,
  },

  alertContent: {
    flex: 1,
  },

  alertTitle: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 15,
  },

  alertText: {
    color: "#91A4C4",
    fontSize: 13,
    marginTop: 5,
    lineHeight: 18,
  },

  climateCard: {
    backgroundColor: "#102846",
    borderRadius: 18,
    padding: 20,
  },

  climateTitle: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },

  climateText: {
    color: "#91A4C4",
    fontSize: 13,
    lineHeight: 20,
    marginTop: 10,
  },

  exploreText: {
    color: "#65C7FF",
    fontWeight: "700",
    marginTop: 15,
  },

  footer: {
    textAlign: "center",
    color: "#536B89",
    fontSize: 11,
    marginTop: 35,
  },

});