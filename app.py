from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema
from smtp_config import conf

app = FastAPI()

class ContactInfo(BaseModel):
    name: str
    email: EmailStr

class ProjectInfo(BaseModel):
    title: str
    description: str

class EmailRequest(BaseModel):
    freelancer: ContactInfo
    contractor: ContactInfo
    project: ProjectInfo

@app.post("/send-contact-emails")
async def send_contact_emails(request: EmailRequest):
    try:
        # Mensagem para o freelancer
        message_freelancer = MessageSchema(
            subject=f"Novo projeto: {request.project.title}",
            recipients=[request.freelancer.email],
            body=(
                f"Olá {request.freelancer.name},\n\n"
                f"Você foi selecionado para o projeto '{request.project.title}'.\n"
                f"Descrição: {request.project.description}\n\n"
                f"Contato do contratante:\n"
                f"Nome: {request.contractor.name}\n"
                f"E-mail: {request.contractor.email}\n"
            ),
            subtype="plain" 
        )

        # Mensagem para o contratante
        message_contractor = MessageSchema(
            subject=f"Contato do freelancer para projeto: {request.project.title}",
            recipients=[request.contractor.email],
            body=(
                f"Olá {request.contractor.name},\n\n"
                f"Você selecionou o freelancer {request.freelancer.name} para o projeto '{request.project.title}'.\n"
                f"Contato do freelancer:\n"
                f"E-mail: {request.freelancer.email}\n"
            ),
            subtype="plain" 
        )

        # FastMail com as configurações SMTP
        fm = FastMail(conf)

        await fm.send_message(message_freelancer)
        await fm.send_message(message_contractor)

        return {"message": "Emails enviados com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar e-mails: {str(e)}")
