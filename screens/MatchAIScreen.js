import React from 'react';
import { View, Text, StyleSheet, Dimensions, StatusBar, TouchableOpacity } from 'react-native';

const { width, height } = Dimensions.get('window');

const MatchAIScreen = () => {
  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <View style={styles.content}>
        <Text style={styles.title}>Match-AI</Text>
        <Text style={styles.subtitle}>Your AI-curated matches</Text>
        
        <View style={styles.infoCard}>
          <Text style={styles.infoTitle}>Complete Questionnaire</Text>
          <Text style={styles.infoText}>
            Answer personality questions to unlock your AI matches. 
            You'll see up to 5 highly compatible matches daily.
          </Text>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Take Questionnaire</Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.matchesPlaceholder}>
          <Text style={styles.matchesText}>AI Matches</Text>
          <Text style={styles.matchesSubtext}>Max 5 matches per day</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: width,
    height: height + 50,
    backgroundColor: '#FFF0F5',
    paddingTop: 50,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    color: '#FFB7C5',
    marginBottom: 30,
    textAlign: 'center',
  },
  infoCard: {
    backgroundColor: '#FFE4E1',
    borderRadius: 15,
    padding: 20,
    marginBottom: 30,
    borderWidth: 1,
    borderColor: '#FFB7C5',
  },
  infoTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
  },
  infoText: {
    fontSize: 16,
    color: '#FFB7C5',
    marginBottom: 20,
    lineHeight: 24,
  },
  button: {
    backgroundColor: '#FF69B4',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 25,
    alignSelf: 'flex-start',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  matchesPlaceholder: {
    flex: 1,
    backgroundColor: '#FFE4E1',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FFB7C5',
    borderStyle: 'dashed',
  },
  matchesText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
  },
  matchesSubtext: {
    fontSize: 16,
    color: '#FFB7C5',
    textAlign: 'center',
  },
});

export default MatchAIScreen; 