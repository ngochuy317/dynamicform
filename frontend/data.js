export const pages = [
    {
        "title": "Contact us",
        "slug": "contact",
        "form": {
            "id": "ckb9j9y3k004i0149ypzxop4r",
            "fields": [
                {
                    "__typename": "FormInput",
                    "name": "Name",
                    "type": "TEXT",
                    "inputLabel": "Name",
                    "placeholder": "Your name",
                    "required": true
                },
                {
                    "__typename": "FormInput",
                    "name": "Email",
                    "type": "EMAIL",
                    "inputLabel": "Email address",
                    "placeholder": "you@example.com",
                    "required": true
                },
                {
                    "__typename": "FormInput",
                    "name": "Tel",
                    "type": "TEL",
                    "inputLabel": "Phone no.",
                    "placeholder": "Your phone number",
                    "required": false
                },
                {
                    "__typename": "FormSelect",
                    "name": "favFramework",
                    "selectLabel": "What's your favorite frontend framework?",
                    "options": [
                        {
                            "value": "React",
                            "option": "React"
                        },
                        {
                            "value": "Vue",
                            "option": "Vue"
                        },
                        {
                            "value": "Angular",
                            "option": "Angular"
                        },
                        {
                            "value": "Svelte",
                            "option": "Svelte"
                        }
                    ],
                    "required": false
                },
                {
                    "__typename": "FormTextarea",
                    "name": "Message",
                    "textareaLabel": "Message",
                    "placeholder": "How can we help?",
                    "required": true
                },
                {
                    "__typename": "FormCheckbox",
                    "name": "Terms",
                    "checkboxLabel": "I agree to the terms and privacy policy.",
                    "required": true
                }
            ]
        }
    }
]