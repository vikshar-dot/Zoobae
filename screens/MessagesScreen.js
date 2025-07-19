import React from 'react';
import { View, Text, StyleSheet, Dimensions, StatusBar } from 'react-native';

const { width, height } = Dimensions.get('window');

const MessagesScreen = () => {
  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent={true}
      />
      <View style={styles.content}>
        <Text style={styles.title}>Messages</Text>
        <Text style={styles.subtitle}>Conversations with your matches</Text>
        
        <View style={styles.messagesPlaceholder}>
          <Text style={styles.messagesText}>Chat Conversations</Text>
          <Text style={styles.messagesSubtext}>Start matching to see conversations here</Text>
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
  messagesPlaceholder: {
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
  messagesText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FF69B4',
    marginBottom: 10,
  },
  messagesSubtext: {
    fontSize: 16,
    color: '#FFB7C5',
    textAlign: 'center',
  },
});

export default MessagesScreen; 