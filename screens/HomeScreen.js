import React from 'react';
import { View, Text, StyleSheet, Dimensions, StatusBar } from 'react-native';

const { width, height } = Dimensions.get('window');

const HomeScreen = () => {
  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <Text style={styles.title}>Welcome to Zoobae!</Text>
      <Text style={styles.subtitle}>Your AI Matchmaker</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: width,
    height: height + 50,
    backgroundColor: '#DC143C',
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 50,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 16,
  },
  subtitle: {
    fontSize: 20,
    color: '#fff',
    fontStyle: 'italic',
  },
});

export default HomeScreen; 