import { useRouter } from "next/router";
import { FormEvent, useState } from "react";
import { useRequestResetPasswordMutation } from "../../../generated/graphql";
import AuthAlert from "../../components/Alert";
import SubmitButton from "../../components/buttons/SubmitButton";
import { AuthForm } from "../../components/forms/auth/AuthForm";
import { AuthInput } from "../../components/forms/auth/LoginForm";

export default function ResetPassword() {
    const [requestPasswordReset, { error }] = useRequestResetPasswordMutation();
    const [showAlert, hideAlert] = useState<boolean>(false);
    const [email, setEmail] = useState<string>("");
    const router = useRouter();
    const pageHref = window.location.href.split('/');
    function handleClick(e: FormEvent) {
        e.preventDefault();
        requestPasswordReset({
            variables: {
                email: email,
                redirectUrl: `${pageHref.slice(0, pageHref.length-1).join('/')}/reset_password`,
            }
        }).then((data) => console.log(data))
        if (!error)
            router.push("/login/request_success")
    }
    return (
        <AuthForm onSubmit={(e) => handleClick(e)}>
            <div className="flex flex-col gap-3">
                <div className="text-2xl">
                    Enter your email address:
                </div>
                <div className="text-sky-700">
                    If your email is registred, you will get an email with reset link
                </div>
            </div>
            <AuthAlert
                show={showAlert}
                text={error?.message}
                hide={() => hideAlert(false)}
            />
            <AuthInput required={true} minLength={3} placeholder="E-Mail" onChange={(e) => setEmail(e.target.value)} type={"email"} />
            <SubmitButton>Send email</SubmitButton>
        </AuthForm>
    )
}