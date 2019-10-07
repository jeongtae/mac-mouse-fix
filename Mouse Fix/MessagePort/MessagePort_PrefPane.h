//
// --------------------------------------------------------------------------
// MessagePort_PrefPane.h
// Created for: Mac Mouse Fix (https://github.com/noah-nuebling/mac-mouse-fix)
// Created by: Noah Nuebling in 2019
// Licensed under MIT
// --------------------------------------------------------------------------
//

#import <Foundation/Foundation.h>


@interface MessagePort_PrefPane : NSObject
+ (void)sendMessageToHelper:(NSString *)message;
//+ (NSString *)sendMessageWithReplyToHelper:(NSString *)message;
@end
