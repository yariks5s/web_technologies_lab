import { Text, TextProps } from "@saleor/ui-kit";
import React from "react";
import { AddressField } from "@/checkout-storefront/lib/globalTypes";
import { useFormattedMessages } from "@/checkout-storefront/hooks/useFormattedMessages";
import { SelectBox, SelectBoxProps } from "@/checkout-storefront/components/SelectBox";
import { Button } from "@/checkout-storefront/components/Button";
import { Address } from "@/checkout-storefront/components/Address";
import { AddressFragment } from "@/checkout-storefront/graphql";
import { addressSelectBoxLabels, addressSelectBoxMessages } from "./messages";

interface AddressSelectBoxProps extends Omit<SelectBoxProps, "children"> {
  address: Partial<Record<AddressField, any>>;
  onEdit: () => void;
  unavailable: boolean;
}

export const AddressSelectBox: React.FC<AddressSelectBoxProps> = ({
  address,
  onEdit,
  unavailable,
  ...rest
}) => {
  const formatMessage = useFormattedMessages();

  const textProps: Pick<TextProps, "color"> = unavailable
    ? {
        color: "secondary",
      }
    : {};

  return (
    <SelectBox {...rest} disabled={unavailable}>
      <div className="w-full flex flex-row justify-between">
        <Address address={address as AddressFragment} {...textProps}>
          {unavailable && (
            <Text size="xs" className="my-1">
              {formatMessage(addressSelectBoxMessages.cantShipToAddress)}
            </Text>
          )}
        </Address>
        <div>
          <Button
            variant="tertiary"
            onClick={(event) => {
              event.stopPropagation();
              onEdit();
            }}
            ariaLabel={formatMessage(addressSelectBoxMessages.editAddress)}
            className="mr-2"
            label={formatMessage(addressSelectBoxLabels.editAddress)}
          />
        </div>
      </div>
    </SelectBox>
  );
};
