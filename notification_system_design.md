# Notification System Design

## Overview
This document outlines the architecture for the notification system.

## Components
1. **Event Trigger:** System events (e.g., service due).
2. **Message Broker:** Celery/Redis for queuing notifications.
3. **Notification Workers:** Processes that handle email/SMS dispatching.
4. **Delivery Handlers:** Third-party integrations (Twilio, SendGrid).

## Flow
- Service layer creates NotificationRecord.
- Dispatcher pushes job to Queue.
- Worker processes job and sends through Gateway.
- Worker updates NotificationRecord status.
