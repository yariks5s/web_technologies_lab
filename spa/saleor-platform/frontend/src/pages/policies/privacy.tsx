import { PoliciesLayout } from "../../components/layouts/PoliciesLayout";
import { PoliciyHeader } from "./impressum";

export default function PrivacyPolicy() {
    return (
        <PoliciesLayout>
            <div className="flex flex-col place-items-center gap-3">
            <PoliciyHeader>
                Data protection
            </PoliciyHeader>
            <PrivacyPolicyList/>
            </div>
        </PoliciesLayout>
    )
}

export function PrivacyPolicyList() {
    return (
        <div className="flex flex-col">
            <div className="flex flex-col gap-2">
                <ListItemHeader number={1}>
                    Introduction and contact details of the person responsible
                </ListItemHeader>
                <ListItemContent>
                    <div className="text-stone-700"><span className="font-bold">1.1</span> We are pleased that you are visiting our website and thank you for your interest. Below we will inform you about how your personal data is handled when you use our website. Personal data is all data with which you can be personally identified.</div>

                    <div className="text-stone-700"><span className="font-bold">1.2</span> The person responsible for data processing on this website within the meaning of the General Data Protection Regulation (GDPR) is Mert Taskin, Am Magnitor 7A, 38100 Braunschweig, Germany, Tel.: 01744880381, Email: info@kreateamshop.de. The person responsible for the processing of personal data is the natural or legal person who, alone or jointly with others, decides on the purposes and means of processing personal data.</div>

                    <div className="text-stone-700"><span className="font-bold">1.3</span> For security reasons and to protect the transmission of personal data and other confidential content (e.g. orders or inquiries to the person responsible), this website uses an SSL or. TLS encryption. You can recognize an encrypted connection by the string “https://” and the lock symbol in your browser bar.</div>
                </ListItemContent>
            </div>
        </div>
    )
}


export function ListItemHeader({ number, children }) {
    return (
        <div className="text-3xl">
            {`${number} ) `}{children}
        </div>
    )
}

export function ListItemContent({ children }) {
    return (
        <div className="flex flex-col gap-1">
            {children}
        </div>
    )
}