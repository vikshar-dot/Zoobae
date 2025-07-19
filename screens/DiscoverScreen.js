import React from 'react';
import { View, Text, StyleSheet, Dimensions, StatusBar } from 'react-native';

const { width, height } = Dimensions.get('window');

const DiscoverScreen = () => {
  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <View style={styles.content}>
        <Text style={styles.title}>Discover</Text>
        <Text style={styles.subtitle}>Swipe profiles to find matches</Text>
        <View style={styles.cardPlaceholder}>
          <Text style={styles.cardText}>Profile Cards</Text>
          <Text style={styles.cardSubtext}>Swipe left/right with compatibility scores</Text>
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
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#FFB7C5',
    marginBottom: 40,
    textAlign: 'center',
  },
  cardPlaceholder: {
    width: width - 40,
    height: 400,
    backgroundColor: '#FFE4E1',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#FFB7C5',
    borderStyle: 'dashed',
  },
  cardText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
  },
  cardSubtext: {
    fontSize: 16,
    color: '#FFB7C5',
    textAlign: 'center',
  },
});

export default DiscoverScreen; 