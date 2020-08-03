DEFAULT_JSON = {
  "time": 1594920529603,
  "blocks": [
    {
      "type": "header",
      "data": {
        "text": "Dinner Rush",
        "level": 1
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Problem Description",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "It is another night at the Darling Canteen and a huge queue of people are waiting for their turn to get a table. The customers are given token numbers as soon as they add their names to the waiting list. The token numbers start from 1 and the next person gets the next number i.e. 2 and so on till n if there are n customers."
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "Some people are extremely tired of waiting and use bribery to move forward. They can bribe the person waiting in the queue just before them and switch positions with them. They can exchange their positions but the token numbers they have will be the same. A person can bribe maximum of 2 people in order to move forward. For example a person with token 3 can bribe the person with token 2 in order to move forward."
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "You see that the queue looks too chaotic as many people are bribing to move forward. Thus you want to find out the minimum number of people who were bribed by looking at the current situation of the queue."
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Input Format",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "Each&nbsp;input&nbsp;consists&nbsp;of&nbsp;two&nbsp;lines"
      }
    },
    {
      "type": "list",
      "data": {
        "style": "ordered",
        "items": [
          "The first line of input contains the number n - Number of people in the queue",
          "The second line of input contains an n token numbers separated by spaces (The current order of the people with tokens)"
        ]
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Output Format",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "Print the minimum number of people who were bribed to attain the current queue. If a person had to bribe more than 2 people to attain the current queue then print -1."
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Constraints",
        "level": 2
      }
    },
    {
      "type": "list",
      "data": {
        "style": "ordered",
        "items": ["1 &lt;= n &lt;= 10^5<br>", "Token numbers are positive"]
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Sample Input 1",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "5"
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "3 1 2 5 4"
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Sample Output 1",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "3"
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "Explanation: 3 will bribe 1 and 2. 5 bribed 4."
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Sample Input 2",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "8"
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "2 1 3 4 8 5 6 7"
      }
    },
    {
      "type": "header",
      "data": {
        "text": "Sample Output 2",
        "level": 2
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "-1"
      }
    },
    {
      "type": "paragraph",
      "data": {
        "text": "Explanation: 8 must bribe 5, 6 and 7 to come at the given position. Thus 8 had to bribe more than 2 people. So output is -1."
      }
    }
  ],
  "version": "2.18.0"
}
